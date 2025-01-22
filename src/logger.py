"""Logging module for GitHub branch protection automation."""
import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional

from .config import config

class Logger:
    """Custom logger class with file and console output."""
    
    def __init__(self, name: str):
        """Initialize logger with both file and console handlers."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, config.log_level.upper()))
        
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Set up both file and console handlers with formatting."""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler with rotation
        file_handler = RotatingFileHandler(
            config.log_file,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, msg: str, *args, **kwargs) -> None:
        """Log debug message."""
        self.logger.debug(msg, *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs) -> None:
        """Log info message."""
        self.logger.info(msg, *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs) -> None:
        """Log warning message."""
        self.logger.warning(msg, *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs) -> None:
        """Log error message."""
        self.logger.error(msg, *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs) -> None:
        """Log critical message."""
        self.logger.critical(msg, *args, **kwargs)
    
    def exception(self, msg: str, *args, exc_info: bool = True, **kwargs) -> None:
        """Log exception with traceback."""
        self.logger.exception(msg, *args, exc_info=exc_info, **kwargs)

# Create a default logger instance
logger = Logger(__name__)
