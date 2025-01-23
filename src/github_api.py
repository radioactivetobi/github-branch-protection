"""GitHub API interaction module for branch protection automation."""
import time
import os
from typing import Dict, List, Optional
from github import Github, GithubException, Repository
from github.Branch import Branch
import requests

from .config import config
from .logger import logger

class GitHubAPI:
    """GitHub API wrapper for managing branch protection rules."""
    
    def __init__(self):
        """Initialize GitHub API connection."""
        self.github = Github(config.github_token)
        self.user = self.github.get_user()
        logger.info(f"Connected to GitHub as {self.user.login}")
    
    def get_default_branch(self, repo_name: str) -> str:
        """Get repository default branch."""
        try:
            repo = self.github.get_repo(f"{config.github_owner}/{repo_name}")
            return repo.default_branch
        except GithubException as e:
            logger.error(f"Failed to get default branch for {repo_name}: {str(e)}")
            raise
    
    def get_branch_protection(self, repo_name: str, branch: str) -> Optional[Dict]:
        """Get current branch protection rules."""
        try:
            repo = self.github.get_repo(f"{config.github_owner}/{repo_name}")
            branch = repo.get_branch(branch)
            return branch.get_protection()
        except GithubException as e:
            if e.status == 404:
                logger.warning(f"No protection rules found for {repo_name}/{branch}")
                return None
            logger.error(f"Failed to get protection rules for {repo_name}/{branch}: {str(e)}")
            raise
    
    def verify_protection_rules(self, protection) -> bool:
        """Verify if protection rules meet requirements."""
        try:
            logger.info("Checking protection rules:")
            
            # Check if protection exists
            if not protection:
                logger.warning("- No protection rules found")
                return False
                
            # Check required reviews
            reviews = getattr(protection, 'required_pull_request_reviews', None)
            if not reviews:
                logger.warning("- Pull request reviews not required")
                return False
                
            if reviews.required_approving_review_count < 1:
                logger.warning("- Insufficient required reviewers")
                return False
                
            # Check admin enforcement - this is a boolean
            enforce_admins = getattr(protection, 'enforce_admins', False)
            if not enforce_admins:
                logger.warning("- Admin enforcement not enabled")
                return False
                
            # Check force pushes - this is a boolean
            allow_force = getattr(protection, 'allow_force_pushes', True)
            if allow_force:
                logger.warning("- Force pushes are allowed")
                return False
                
            # Check deletions - this is a boolean
            allow_delete = getattr(protection, 'allow_deletions', True)
            if allow_delete:
                logger.warning("- Branch deletions are allowed")
                return False
                
            logger.info("All protection rules verified successfully")
            return True
            
        except Exception as e:
            logger.error(f"Protection rule verification error: {str(e)}")
            return False
            
    def get_protection_issues(self, protection) -> List[str]:
        """Get list of protection rule issues."""
        issues = []
        
        if not protection:
            issues.append("No protection rules configured")
            return issues
            
        try:
            # Check required reviews
            reviews = getattr(protection, 'required_pull_request_reviews', None)
            if not reviews:
                issues.append("Pull request reviews not required")
            elif reviews.required_approving_review_count < 1:
                issues.append("Insufficient required reviewers")
                
            # Check admin enforcement
            enforce_admins = getattr(protection, 'enforce_admins', False)
            if not enforce_admins:
                issues.append("Admin enforcement not enabled")
                
            # Check branch restrictions
            if getattr(protection, 'allow_force_pushes', True):
                issues.append("Force pushes are allowed")
            if getattr(protection, 'allow_deletions', True):
                issues.append("Branch deletions are allowed")
                
        except Exception as e:
            issues.append(f"Invalid protection configuration: {str(e)}")
            
        return issues
        
    def set_branch_protection(self, repo_name: str, branch: str) -> None:
        """Set branch protection rules."""
        try:
            repo = self.github.get_repo(f"{config.github_owner}/{repo_name}")
            branch = repo.get_branch(branch)
            
            logger.info(f"Setting protection rules for {repo_name}/{branch.name}")
            
            branch.edit_protection(
                # Required status checks
                strict=True,
                contexts=[],
                
                # Required PR reviews
                required_approving_review_count=1,
                dismiss_stale_reviews=True,
                require_code_owner_reviews=False,
                
                # Admin enforcement
                enforce_admins=True,
                
                # Branch restrictions
                allow_force_pushes=False,
                allow_deletions=False,
                required_linear_history=True
            )
            
            logger.info(f"Successfully set protection rules for {repo_name}/{branch.name}")
            
        except GithubException as e:
            logger.error(f"Failed to set protection rules for {repo_name}/{branch}: {str(e)}")
            raise
    
    @staticmethod
    def read_repos_from_file(file_path: str) -> List[str]:
        """Read repository names from file."""
        try:
            with open(file_path, 'r') as f:
                return [line.strip() for line in f 
                        if line.strip() and not line.startswith('#')]
        except Exception as e:
            logger.error(f"Failed to read repository list from {file_path}: {str(e)}")
            raise

# Create a global GitHub API instance
github_api = GitHubAPI()
