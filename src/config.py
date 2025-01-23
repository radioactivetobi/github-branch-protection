"""Configuration module for branch protection automation."""
import os
from typing import List, Optional
from dotenv import load_dotenv

class Config:
    """Configuration class."""
    
    def __init__(self):
        """Initialize configuration."""
        load_dotenv()
        
        # Initialize with None
        self.github_token: Optional[str] = None
        self.github_owner: Optional[str] = None
        self.repositories: Optional[List[str]] = None
        
        # Load from environment
        self.github_token = self._get_required('GITHUB_TOKEN')
        self.github_owner = self._get_required('GITHUB_OWNER')
        
        # Get repositories from environment or command line
        repos_env = os.getenv('REPOSITORIES')
        if repos_env:
            self.repositories = [r.strip() for r in repos_env.split() if r.strip()]
        
        # Branch protection settings
        self.required_approvals = int(os.getenv('REQUIRED_APPROVALS', '1'))
        self.enforce_admins = os.getenv('ENFORCE_ADMINS', 'true').lower() == 'true'
        self.require_ci = os.getenv('REQUIRE_CI', 'true').lower() == 'true'
        
        # Logging settings
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_file = os.getenv('LOG_FILE', 'branch_protection.log')
    
    def _get_required(self, key: str) -> str:
        """Get required environment variable."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable '{key}' is not set")
        return value
    
    def validate(self):
        """Validate configuration."""
        if not self.repositories:
            raise ValueError("No repositories specified. Use --repos, --repos-file, or REPOSITORIES environment variable")
        
        if not all(self.repositories):
            raise ValueError("Empty repository name in list")

# Create a global config instance
config = Config()
