"""Configuration module for branch protection automation."""
import os
from typing import List, Optional
from dotenv import load_dotenv

class Config:
    """Configuration class."""
    
    def __init__(self):
        """Initialize configuration."""
        load_dotenv()
        
        # Required settings
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_owner = os.getenv('GITHUB_OWNER')
        
        # Optional settings
        self.repositories = self._get_repositories()
        self.verify_only = os.getenv('VERIFY_ONLY', 'false').lower() == 'true'
        
        # Branch protection settings
        self.required_approvals = int(os.getenv('REQUIRED_APPROVALS', '1'))
        self.enforce_admins = os.getenv('ENFORCE_ADMINS', 'true').lower() == 'true'
        self.require_ci = os.getenv('REQUIRE_CI', 'true').lower() == 'true'
        
        # Logging settings
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_file = os.getenv('LOG_FILE', 'branch_protection.log')
    
    def _get_repositories(self) -> List[str]:
        """Get repositories from environment."""
        repos = os.getenv('REPOSITORIES', '')
        if repos:
            return [r.strip() for r in repos.split() if r.strip()]
        return []
    
    def validate(self):
        """Validate configuration."""
        if not self.github_token:
            raise ValueError("GitHub token not set. Set GITHUB_TOKEN environment variable.")
            
        if not self.github_owner:
            raise ValueError("GitHub owner not set. Set GITHUB_OWNER environment variable.")

# Create a global config instance
config = Config()
