"""
Configuration settings for the Telegram bot
"""

import os
import logging

logger = logging.getLogger(__name__)

class Config:
    """Configuration class for bot settings"""
    
    def __init__(self):
        # Telegram Bot Token
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.telegram_token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        
        # Gemini API Key
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Rate limiting settings
        self.rate_limit_per_user = int(os.getenv("RATE_LIMIT_PER_USER", "10"))  # requests per minute
        self.rate_limit_window = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds
        
        # Bot settings
        self.max_message_length = int(os.getenv("MAX_MESSAGE_LENGTH", "4096"))
        self.timeout = int(os.getenv("REQUEST_TIMEOUT", "30"))  # seconds
        
        # Logging settings
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        self.log_file = os.getenv("LOG_FILE", "bot.log")
        
        # Debug mode
        self.debug_mode = os.getenv("DEBUG_MODE", "False").lower() == "true"
        
        logger.info("Configuration loaded successfully")
        
        if self.debug_mode:
            logger.info(f"Rate limit: {self.rate_limit_per_user} requests per {self.rate_limit_window} seconds")
            logger.info(f"Max message length: {self.max_message_length}")
            logger.info(f"Request timeout: {self.timeout} seconds")
    
    def validate(self):
        """Validate configuration settings"""
        if not self.telegram_token:
            raise ValueError("Telegram bot token is required")
        
        if not self.gemini_api_key:
            raise ValueError("Gemini API key is required")
        
        if self.rate_limit_per_user <= 0:
            raise ValueError("Rate limit per user must be positive")
        
        if self.rate_limit_window <= 0:
            raise ValueError("Rate limit window must be positive")
        
        if self.max_message_length <= 0:
            raise ValueError("Max message length must be positive")
        
        if self.timeout <= 0:
            raise ValueError("Request timeout must be positive")
        
        logger.info("Configuration validation passed")
