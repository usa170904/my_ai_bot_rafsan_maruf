#!/usr/bin/env python3
"""
Multilingual Telegram Bot with Google Gemini Integration
Main entry point for the bot application
"""

import asyncio
import logging
import os
import sys
from bot import TelegramBot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['TELEGRAM_BOT_TOKEN', 'GEMINI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set the following environment variables:")
        logger.error("export TELEGRAM_BOT_TOKEN='your_telegram_bot_token'")
        logger.error("export GEMINI_API_KEY='your_gemini_api_key'")
        sys.exit(1)

def main():
    """Main function to start the bot"""
    try:
        # Check environment variables
        check_environment()
        
        logger.info("Starting Multilingual Telegram Bot with Gemini Integration...")
        
        # Create and start the bot
        bot = TelegramBot()
        bot.start()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)
