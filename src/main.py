"""Main entry point for GitHub branch protection automation."""
import argparse
import sys
from typing import List, Dict

from .config import config
from .logger import logger
from .github_api import github_api
from .report_generator import generate_protection_report

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Automate GitHub branch protection rules across repositories."
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify existing protection rules without modifying them"
    )
    parser.add_argument(
        "--repos",
        nargs="+",
        help="Space-separated list of repository names to process"
    )
    parser.add_argument(
        "--repos-file",
        type=str,
        help="Path to text file containing repository names (one per line)"
    )
    return parser.parse_args()

def verify_repository(repo_name: str) -> Dict:
    """Verify branch protection rules for a single repository."""
    try:
        default_branch = github_api.get_default_branch(repo_name)
        protection = github_api.get_branch_protection(repo_name, default_branch)
        
        # Check if protection exists and meets requirements
        if protection and github_api.verify_protection_rules(protection):
            logger.info(f"[PASS] {repo_name}: Branch protection rules are properly configured")
            return {"name": repo_name, "status": True, "issues": []}
        else:
            issues = github_api.get_protection_issues(protection)
            logger.warning(f"[FAIL] {repo_name}: Branch protection rules need updates")
            return {"name": repo_name, "status": False, "issues": issues}
            
    except Exception as e:
        logger.error(f"Failed to verify {repo_name}: {str(e)}")
        return {"name": repo_name, "status": False, "issues": [str(e)]}

def process_repositories(repositories: List[str], verify_only: bool = False) -> List[Dict]:
    """Process a list of repositories."""
    results = []
    for repo in repositories:
        try:
            if verify_only:
                results.append(verify_repository(repo))
            else:
                # Initial verification
                logger.info(f"Verifying current protection rules for {repo}")
                initial_check = verify_repository(repo)
                
                # If protection is already properly configured, skip
                if initial_check["status"]:
                    logger.info(f"[PASS] {repo}: Already properly configured")
                    results.append(initial_check)
                    continue
                    
                # Apply protection rules
                logger.info(f"Applying protection rules to {repo}")
                default_branch = github_api.get_default_branch(repo)
                github_api.set_branch_protection(repo, default_branch)
                
                # Verify after applying
                logger.info(f"Verifying applied protection rules for {repo}")
                final_check = verify_repository(repo)
                results.append(final_check)
                
        except Exception as e:
            logger.error(f"Failed to process {repo}: {str(e)}")
            results.append({
                "name": repo,
                "status": False,
                "issues": [str(e)]
            })
            
    return results

def main() -> int:
    """Main entry point."""
    try:
        args = parse_args()
        
        # Determine repository list
        if args.repos:
            repositories = args.repos
        elif args.repos_file:
            repositories = github_api.read_repos_from_file(args.repos_file)
        else:
            repositories = config.repositories
            
        if not repositories:
            logger.error("No repositories specified. Use --repos or --repos-file")
            return 1
            
        # Process repositories
        results = process_repositories(repositories, args.verify_only)
        
        # Generate report
        report_path = generate_protection_report(results)
        logger.info(f"Report generated: {report_path}")
        
        # Return success only if all repositories are properly protected
        return 0 if all(r["status"] for r in results) else 1
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130
    except Exception as e:
        logger.exception("Unexpected error occurred")
        return 1

if __name__ == "__main__":
    sys.exit(main())
