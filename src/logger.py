"""Logging configuration module."""
import logging
import os
import sys
from datetime import datetime

class Logger:
    """Custom logger class."""
    
    def __init__(self):
        """Initialize logger."""
        self.logger = logging.getLogger('src.logger')
        self.logger.setLevel(logging.INFO)
        
        # Create formatters
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            '%Y-%m-%d %H:%M:%S'
        )
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        
    def info(self, msg, *args, **kwargs):
        """Log info message."""
        self.logger.info(msg, *args, **kwargs)
        
    def warning(self, msg, *args, **kwargs):
        """Log warning message."""
        self.logger.warning(msg, *args, **kwargs)
        
    def error(self, msg, *args, **kwargs):
        """Log error message."""
        self.logger.error(msg, *args, **kwargs)
        
    def exception(self, msg, *args, **kwargs):
        """Log exception message."""
        self.logger.exception(msg, *args, **kwargs)

logger = Logger()
