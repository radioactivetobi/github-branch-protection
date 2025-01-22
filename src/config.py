"""Configuration module for GitHub branch protection automation."""
import os
from typing import List
from dotenv import load_dotenv

class Config:
    """Configuration class to manage environment variables and settings."""
    
    def __init__(self):
        """Initialize configuration by loading environment variables."""
        load_dotenv()
        
        # GitHub settings
        self.github_token = self._get_required('GITHUB_TOKEN')
        self.github_owner = self._get_required('GITHUB_OWNER')
        self.repositories = self._get_list('REPOSITORIES')
        
        # Branch protection settings
        self.required_approvals = int(os.getenv('REQUIRED_APPROVALS', '1'))
        self.enforce_admins = os.getenv('ENFORCE_ADMINS', 'true').lower() == 'true'
        self.require_ci = os.getenv('REQUIRE_CI', 'true').lower() == 'true'
        
        # Logging settings
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_file = os.getenv('LOG_FILE', 'branch_protection.log')
    
    def _get_required(self, key: str) -> str:
        """Get a required environment variable or raise an error."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable '{key}' is not set")
        return value
    
    def _get_list(self, key: str) -> List[str]:
        """Get a comma-separated environment variable as a list."""
        value = self._get_required(key)
        return [item.strip() for item in value.split(',') if item.strip()]
    
    def validate(self) -> None:
        """Validate the configuration."""
        if not self.repositories:
            raise ValueError("No repositories specified")
        if self.required_approvals < 1:
            raise ValueError("Required approvals must be at least 1")

# Create a global config instance
config = Config()
