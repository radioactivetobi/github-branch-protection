"""GitHub API interaction module for branch protection automation."""
import time
from typing import List, Optional
from github import Github, GithubException, Repository
from github.Branch import Branch
import requests

from .config import config
from .logger import logger

class GitHubAPI:
    """GitHub API wrapper for managing branch protection rules."""
    
    def __init__(self, token, owner):
        """Initialize GitHub API client."""
        self.token = token
        self.owner = owner
        try:
            self.github = Github(token)
            logger.info(f"Connected to GitHub as {self.github.get_user().login}")
        except Exception as e:
            logger.error(f"Failed to initialize GitHub client: {str(e)}")
            raise
    
    def _get_repository(self, repo_name: str) -> Repository.Repository:
        """Get a GitHub repository object."""
        try:
            return self.github.get_repo(f"{self.owner}/{repo_name}")
        except GithubException as e:
            logger.error(f"Failed to access repository {repo_name}: {str(e)}")
            raise
    
    def _get_default_branch(self, repo: Repository.Repository) -> str:
        """Get the default branch name from a repository."""
        return repo.default_branch
    
    def set_branch_protection(self, repo_name: str) -> None:
        """Set branch protection rules using repository ruleset."""
        logger.info(f"Setting branch protection ruleset for {repo_name}")
        
        # Get repository and its default branch
        repo = self.github.get_repo(f"{self.owner}/{repo_name}")
        default_branch = repo.default_branch
        logger.info(f"Default branch is: {default_branch}")
        
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/vnd.github.v4+json'
        }
        
        # Query to get repository ID
        id_query = """
        query($owner: String!, $name: String!) {
            repository(owner: $owner, name: $name) {
                id
                defaultBranchRef {
                    name
                }
            }
        }
        """
        
        variables = {
            "owner": self.owner,
            "name": repo_name
        }
        
        # Get the repository ID
        response = requests.post(
            'https://api.github.com/graphql',
            json={'query': id_query, 'variables': variables},
            headers=headers
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get repository ID: {response.text}")
        
        repo_id = response.json()['data']['repository']['id']
        
        # Now set the branch protection using ruleset
        protection_query = """
        mutation($repositoryId: ID!, $pattern: String!) {
            createBranchProtectionRule(input: {
                repositoryId: $repositoryId,
                pattern: $pattern,
                requiresApprovingReviews: true,
                requiredApprovingReviewCount: 1,
                requiresStatusChecks: true,
                requiresStrictStatusChecks: true,
                dismissesStaleReviews: true,
                restrictsReviewDismissals: true,
                isAdminEnforced: true,
                allowsForcePushes: false,
                allowsDeletions: false
            }) {
                branchProtectionRule {
                    id
                    pattern
                }
            }
        }
        """
        
        variables = {
            "repositoryId": repo_id,
            "pattern": default_branch
        }
        
        response = requests.post(
            'https://api.github.com/graphql',
            json={'query': protection_query, 'variables': variables},
            headers=headers
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to set branch protection: {response.text}")
        
        result = response.json()
        if 'errors' in result:
            raise Exception(f"GraphQL error: {result['errors']}")
            
        logger.info(f"Successfully set branch protection for {repo_name} on branch {default_branch}")
    
    def process_repositories(self) -> None:
        """Process all configured repositories."""
        for repo_name in config.repositories:
            try:
                self.set_branch_protection(repo_name)
            except GithubException as e:
                logger.error(f"Skipping repository {repo_name} due to error: {str(e)}")
                continue
            except Exception as e:
                logger.exception(f"Unexpected error processing {repo_name}")
                continue
            
            # Add delay between repositories to avoid rate limiting
            time.sleep(1)
    
    def verify_protection(self, repo_name: str) -> dict:
        """Verify branch protection ruleset and return detailed results."""
        logger.info(f"Verifying branch protection for {repo_name}")
        
        try:
            # Get repository and its default branch
            repo = self.github.get_repo(f"{self.owner}/{repo_name}")
            default_branch = repo.default_branch
            
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Accept': 'application/vnd.github.v4+json'
            }
            
            query = """
            query($owner: String!, $name: String!) {
                repository(owner: $owner, name: $name) {
                    branchProtectionRules(first: 100) {
                        nodes {
                            pattern
                            requiresApprovingReviews
                            requiredApprovingReviewCount
                            isAdminEnforced
                            allowsForcePushes
                            allowsDeletions
                        }
                    }
                }
            }
            """
            
            variables = {
                "owner": self.owner,
                "name": repo_name
            }
            
            response = requests.post(
                'https://api.github.com/graphql',
                json={'query': query, 'variables': variables},
                headers=headers
            )
            
            if response.status_code != 200:
                return {
                    'repository': repo_name,
                    'status': False,
                    'default_branch': default_branch,
                    'issues': ['Failed to query protection rules']
                }
            
            return self._verify_protection_rules(response.json(), default_branch, repo_name)
            
        except Exception as e:
            return {
                'repository': repo_name,
                'status': False,
                'issues': [str(e)]
            }

    def _verify_protection_rules(self, response_data, default_branch, repo_name) -> dict:
        """Verify the branch protection rules and return detailed results."""
        result = {
            'repository': repo_name,
            'status': False,
            'default_branch': default_branch,
            'issues': []
        }
        
        try:
            protection_rules = response_data['data']['repository']['branchProtectionRules']['nodes']
            
            if not protection_rules:
                result['issues'].append("No branch protection rules found")
                return result
            
            for rule in protection_rules:
                if rule['pattern'] == default_branch:
                    # Check required reviews
                    if not rule.get('requiresApprovingReviews'):
                        result['issues'].append("Required reviews not enabled")
                    
                    if rule.get('requiredApprovingReviewCount', 0) < 1:
                        result['issues'].append("Required review count is less than 1")
                    
                    # Check force push and deletion restrictions
                    if rule.get('allowsForcePushes'):
                        result['issues'].append("Force pushes are allowed")
                    
                    if rule.get('allowsDeletions'):
                        result['issues'].append("Branch deletion is allowed")
                    
                    if not rule.get('isAdminEnforced'):
                        result['issues'].append("Rules are not enforced for administrators")
                    
                    # Set status based on issues
                    result['status'] = len(result['issues']) == 0
                    return result
            
            result['issues'].append(f"No protection rule found for default branch: {default_branch}")
            return result
            
        except Exception as e:
            result['issues'].append(f"Error verifying protection rules: {str(e)}")
            return result

# Create a global GitHub API instance
github_api = GitHubAPI(config.github_token, config.github_owner)
