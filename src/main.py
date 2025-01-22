"""Main entry point for GitHub branch protection automation."""
import argparse
import sys
from typing import List, Optional, Dict

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

def read_repos_from_file(file_path: str) -> List[str]:
    """Read repository names from a text file."""
    try:
        with open(file_path, 'r') as f:
            # Read lines, strip whitespace, and filter out empty lines
            repos = [line.strip() for line in f.readlines()]
            repos = [repo for repo in repos if repo and not repo.startswith('#')]
            
            if not repos:
                logger.warning(f"No repository names found in {file_path}")
                return []
                
            logger.info(f"Loaded {len(repos)} repositories from {file_path}")
            return repos
    except Exception as e:
        logger.error(f"Failed to read repositories from {file_path}: {str(e)}")
        raise

def verify_repositories(repositories: List[str]) -> List[Dict]:
    """Verify branch protection rules for specified repositories."""
    results = []
    for repo in repositories:
        result = github_api.verify_protection(repo)
        results.append(result)
        if not result['status']:
            logger.error(f"Branch protection verification failed for {repo}")
    return results

def main() -> int:
    """Main execution function."""
    try:
        args = parse_args()
        
        # Determine repository list from arguments
        if args.repos_file:
            config.repositories = read_repos_from_file(args.repos_file)
        elif args.repos:
            config.repositories = args.repos
        
        if not config.repositories:
            logger.error("No repositories specified. Use --repos or --repos-file")
            return 1
        
        config.validate()
        
        logger.info("Starting branch protection automation")
        logger.info(f"Processing repositories: {', '.join(config.repositories)}")
        
        if args.verify_only:
            logger.info("Running in verify-only mode")
            results = verify_repositories(config.repositories)
            
            # Generate report
            report_path = generate_protection_report(results)
            logger.info(f"Report generated: {report_path}")
            
            return 0 if all(r['status'] for r in results) else 1
        
        # Process repositories
        github_api.process_repositories()
        
        # Verify protection rules and generate report
        logger.info("Verifying branch protection rules")
        results = verify_repositories(config.repositories)
        report_path = generate_protection_report(results)
        logger.info(f"Report generated: {report_path}")
        
        if all(r['status'] for r in results):
            logger.info("Branch protection automation completed successfully")
            return 0
        else:
            logger.error("Branch protection verification failed for one or more repositories")
            return 1
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130
    except Exception as e:
        logger.exception("Unexpected error occurred")
        return 1

if __name__ == "__main__":
    sys.exit(main())
