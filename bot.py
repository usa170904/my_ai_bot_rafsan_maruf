"""
Main Telegram Bot implementation with Gemini integration
"""

import asyncio
import logging
from typing import Optional
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode, ChatAction

from config import Config
from gemini_client import GeminiClient
from language_handler import LanguageHandler
from commands import Commands
from rate_limiter import RateLimiter
from utils import format_code_response, escape_markdown

logger = logging.getLogger(__name__)

class TelegramBot:
    """Main Telegram bot class"""
    
    def __init__(self):
        self.config = Config()
        self.gemini_client = GeminiClient()
        self.language_handler = LanguageHandler()
        self.rate_limiter = RateLimiter()
        self.commands = Commands(self.gemini_client, self.language_handler)
        
        # Initialize the application
        self.application = Application.builder().token(self.config.telegram_token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("code", self.code_command))
        self.application.add_handler(CommandHandler("app", self.app_command))
        self.application.add_handler(CommandHandler("web", self.web_command))
        self.application.add_handler(CommandHandler("ask", self.ask_command))
        self.application.add_handler(CommandHandler("lang", self.language_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("ai", self.ai_command))
        self.application.add_handler(CommandHandler("ml", self.ml_command))
        self.application.add_handler(CommandHandler("mobile", self.mobile_command))
        self.application.add_handler(CommandHandler("db", self.database_command))
        self.application.add_handler(CommandHandler("api", self.api_command))
        
        # Message handler for general queries
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
        
        # Set commands on startup - will be called automatically when polling starts
    
    def start(self):
        """Start the bot"""
        try:
            logger.info("Bot started successfully")
            
            # Start polling with post_init hook for setting commands
            async def post_init(app):
                await self._set_bot_commands()
            
            self.application.post_init = post_init
            self.application.run_polling(drop_pending_updates=True)
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
    
    async def _set_bot_commands(self):
        """Set bot commands for better UX"""
        commands = [
            BotCommand("start", "Start the bot / বট শুরু করুন"),
            BotCommand("help", "Show help / সাহায্য দেখুন"),
            BotCommand("code", "Generate code / কোড তৈরি করুন"),
            BotCommand("app", "Create app code / অ্যাপ কোড তৈরি করুন"),
            BotCommand("web", "Create website code / ওয়েবসাইট কোড তৈরি করুন"),
            BotCommand("ai", "AI/ML projects / AI/ML প্রোজেক্ট"),
            BotCommand("mobile", "Mobile app dev / মোবাইল অ্যাপ"),
            BotCommand("api", "API development / API ডেভেলপমেন্ট"),
            BotCommand("ask", "Ask any question / যেকোনো প্রশ্ন করুন"),
            BotCommand("lang", "Change language / ভাষা পরিবর্তন করুন"),
            BotCommand("status", "Bot status / বট স্ট্যাটাস"),
        ]
        
        await self.application.bot.set_my_commands(commands)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
        
        welcome_message = self.language_handler.get_message("welcome", user_lang)
        
        await update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
        help_message = self.language_handler.get_message("help", user_lang)
        
        await update.message.reply_text(
            help_message,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def code_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /code command for code generation"""
        user_id = update.effective_user.id
        
        # Check rate limit
        if not self.rate_limiter.check_rate_limit(user_id):
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            rate_limit_msg = self.language_handler.get_message("rate_limit", user_lang)
            await update.message.reply_text(rate_limit_msg)
            return
        
        # Get the code request
        request_text = " ".join(context.args) if context.args else ""
        
        if not request_text:
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            usage_msg = self.language_handler.get_message("code_usage", user_lang)
            await update.message.reply_text(usage_msg)
            return
        
        await self._process_code_request(update, request_text, "code")
    
    async def app_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /app command for app development"""
        user_id = update.effective_user.id
        
        if not self.rate_limiter.check_rate_limit(user_id):
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            rate_limit_msg = self.language_handler.get_message("rate_limit", user_lang)
            await update.message.reply_text(rate_limit_msg)
            return
        
        request_text = " ".join(context.args) if context.args else ""
        
        if not request_text:
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            usage_msg = self.language_handler.get_message("app_usage", user_lang)
            await update.message.reply_text(usage_msg)
            return
        
        await self._process_code_request(update, request_text, "app")
    
    async def web_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /web command for website development"""
        user_id = update.effective_user.id
        
        if not self.rate_limiter.check_rate_limit(user_id):
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            rate_limit_msg = self.language_handler.get_message("rate_limit", user_lang)
            await update.message.reply_text(rate_limit_msg)
            return
        
        request_text = " ".join(context.args) if context.args else ""
        
        if not request_text:
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            usage_msg = self.language_handler.get_message("web_usage", user_lang)
            await update.message.reply_text(usage_msg)
            return
        
        await self._process_code_request(update, request_text, "web")
    
    async def ask_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ask command for general questions"""
        user_id = update.effective_user.id
        
        if not self.rate_limiter.check_rate_limit(user_id):
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            rate_limit_msg = self.language_handler.get_message("rate_limit", user_lang)
            await update.message.reply_text(rate_limit_msg)
            return
        
        question = " ".join(context.args) if context.args else ""
        
        if not question:
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            usage_msg = self.language_handler.get_message("ask_usage", user_lang)
            await update.message.reply_text(usage_msg)
            return
        
        await self._process_general_question(update, question)
    
    async def language_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /lang command for language switching"""
        user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
        lang_message = self.language_handler.get_message("language_info", user_lang)
        
        await update.message.reply_text(lang_message)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
        status_message = self.language_handler.get_message("status", user_lang)
        
        await update.message.reply_text(status_message)
    
    async def ai_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ai command for AI/ML projects"""
        user_id = update.effective_user.id
        
        if not self.rate_limiter.check_rate_limit(user_id):
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            rate_limit_msg = self.language_handler.get_message("rate_limit", user_lang)
            await update.message.reply_text(rate_limit_msg)
            return
        
        request_text = " ".join(context.args) if context.args else ""
        
        if not request_text:
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            if user_lang == 'bn':
                usage_msg = "🤖 ব্যবহার: `/ai <আপনার AI/ML প্রোজেক্ট>`\n\nউদাহরণ: `/ai ইমেজ ক্লাসিফিকেশন মডেল তৈরি করুন`"
            else:
                usage_msg = "🤖 Usage: `/ai <your AI/ML project>`\n\nExample: `/ai create an image classification model`"
            await update.message.reply_text(usage_msg)
            return
        
        await self._process_code_request(update, request_text, "ai")
    
    async def ml_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ml command for machine learning"""
        user_id = update.effective_user.id
        
        if not self.rate_limiter.check_rate_limit(user_id):
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            rate_limit_msg = self.language_handler.get_message("rate_limit", user_lang)
            await update.message.reply_text(rate_limit_msg)
            return
        
        request_text = " ".join(context.args) if context.args else ""
        
        if not request_text:
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            if user_lang == 'bn':
                usage_msg = "🧠 ব্যবহার: `/ml <আপনার মেশিন লার্নিং প্রোজেক্ট>`\n\nউদাহরণ: `/ml টেক্সট সেন্টিমেন্ট এনালাইসিস`"
            else:
                usage_msg = "🧠 Usage: `/ml <your machine learning project>`\n\nExample: `/ml text sentiment analysis`"
            await update.message.reply_text(usage_msg)
            return
        
        await self._process_code_request(update, request_text, "ml")
    
    async def mobile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /mobile command for mobile app development"""
        user_id = update.effective_user.id
        
        if not self.rate_limiter.check_rate_limit(user_id):
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            rate_limit_msg = self.language_handler.get_message("rate_limit", user_lang)
            await update.message.reply_text(rate_limit_msg)
            return
        
        request_text = " ".join(context.args) if context.args else ""
        
        if not request_text:
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            if user_lang == 'bn':
                usage_msg = "📱 ব্যবহার: `/mobile <আপনার মোবাইল অ্যাপ আইডিয়া>`\n\nউদাহরণ: `/mobile ফ্লাটারে ই-কমার্স অ্যাপ`"
            else:
                usage_msg = "📱 Usage: `/mobile <your mobile app idea>`\n\nExample: `/mobile e-commerce app in Flutter`"
            await update.message.reply_text(usage_msg)
            return
        
        await self._process_code_request(update, request_text, "mobile")
    
    async def database_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /db command for database development"""
        user_id = update.effective_user.id
        
        if not self.rate_limiter.check_rate_limit(user_id):
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            rate_limit_msg = self.language_handler.get_message("rate_limit", user_lang)
            await update.message.reply_text(rate_limit_msg)
            return
        
        request_text = " ".join(context.args) if context.args else ""
        
        if not request_text:
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            if user_lang == 'bn':
                usage_msg = "🗄️ ব্যবহার: `/db <আপনার ডাটাবেস প্রোজেক্ট>`\n\nউদাহরণ: `/db ইউজার ম্যানেজমেন্ট সিস্টেম`"
            else:
                usage_msg = "🗄️ Usage: `/db <your database project>`\n\nExample: `/db user management system`"
            await update.message.reply_text(usage_msg)
            return
        
        await self._process_code_request(update, request_text, "database")
    
    async def api_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /api command for API development"""
        user_id = update.effective_user.id
        
        if not self.rate_limiter.check_rate_limit(user_id):
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            rate_limit_msg = self.language_handler.get_message("rate_limit", user_lang)
            await update.message.reply_text(rate_limit_msg)
            return
        
        request_text = " ".join(context.args) if context.args else ""
        
        if not request_text:
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            if user_lang == 'bn':
                usage_msg = "🔗 ব্যবহার: `/api <আপনার API প্রোজেক্ট>`\n\nউদাহরণ: `/api RESTful API for blog`"
            else:
                usage_msg = "🔗 Usage: `/api <your API project>`\n\nExample: `/api RESTful API for blog`"
            await update.message.reply_text(usage_msg)
            return
        
        await self._process_code_request(update, request_text, "api")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle general text messages"""
        user_id = update.effective_user.id
        message_text = update.message.text
        
        # Check for creator questions first
        creator_keywords = [
            'কে তৈরি', 'কে বানিয়েছে', 'কে ডেভেলপ', 'কে বানায়', 'তৈরি করেছে', 'তৈরি করছে',
            'who created', 'who developed', 'who made', 'who built', 'created by', 'developed by'
        ]
        
        message_lower = message_text.lower()
        is_creator_question = any(keyword in message_lower for keyword in creator_keywords)
        
        if is_creator_question:
            language = self.language_handler.detect_message_language(message_text)
            if language == "bn":
                creator_response = "আমাকে Rafsan Maruf তৈরি করেছেন।"
            else:
                creator_response = "I was created by Rafsan Maruf."
            
            await update.message.reply_text(creator_response)
            return
        
        # Check rate limit
        if not self.rate_limiter.check_rate_limit(user_id):
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            rate_limit_msg = self.language_handler.get_message("rate_limit", user_lang)
            await update.message.reply_text(rate_limit_msg)
            return
        
        # Enhanced detection logic
        is_code_request = self.language_handler.is_code_request(message_text)
        
        # Log for debugging
        logger.info(f"Message: {message_text[:50]}... | Is code request: {is_code_request}")
        
        # Try both approaches - if one fails, try the other
        try:
            if is_code_request:
                await self._process_code_request(update, message_text, "general")
            else:
                await self._process_general_question(update, message_text)
        except Exception as e:
            logger.error(f"Error in primary processing: {e}")
            # Fallback to alternative processing
            try:
                if not is_code_request:
                    await self._process_code_request(update, message_text, "general")
                else:
                    await self._process_general_question(update, message_text)
            except Exception as e2:
                logger.error(f"Error in fallback processing: {e2}")
                # Final fallback - direct response
                user_lang = self.language_handler.detect_message_language(message_text)
                if user_lang == 'bn':
                    await update.message.reply_text("দুঃখিত, একটি ত্রুটি হয়েছে। আবার চেষ্টা করুন।")
                else:
                    await update.message.reply_text("Sorry, there was an error. Please try again.")
    
    async def _process_code_request(self, update: Update, request: str, request_type: str):
        """Process code generation requests"""
        await update.message.chat.send_action(ChatAction.TYPING)
        
        try:
            user_lang = self.language_handler.detect_message_language(request)
            response = await self.commands.generate_code(request, request_type, user_lang)
            
            # Format and send the response
            formatted_response = format_code_response(response)
            
            # Split long messages if needed
            if len(formatted_response) > 4096:
                chunks = [formatted_response[i:i+4096] for i in range(0, len(formatted_response), 4096)]
                for chunk in chunks:
                    try:
                        await update.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN)
                    except Exception as e:
                        # If markdown fails, send as plain text
                        await update.message.reply_text(chunk)
            else:
                try:
                    await update.message.reply_text(formatted_response, parse_mode=ParseMode.MARKDOWN)
                except Exception as e:
                    # If markdown fails, send as plain text
                    await update.message.reply_text(formatted_response)
                
        except Exception as e:
            logger.error(f"Error processing code request: {e}")
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            error_msg = self.language_handler.get_message("error", user_lang)
            await update.message.reply_text(error_msg)
    
    async def _process_general_question(self, update: Update, question: str):
        """Process general questions"""
        await update.message.chat.send_action(ChatAction.TYPING)
        
        try:
            user_lang = self.language_handler.detect_message_language(question)
            response = await self.commands.answer_question(question, user_lang)
            
            # Split long messages if needed and send without markdown to avoid parsing issues
            if len(response) > 4096:
                chunks = [response[i:i+4096] for i in range(0, len(response), 4096)]
                for chunk in chunks:
                    await update.message.reply_text(chunk)
            else:
                await update.message.reply_text(response)
                
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            user_lang = self.language_handler.detect_user_language(update.effective_user.language_code)
            error_msg = self.language_handler.get_message("error", user_lang)
            await update.message.reply_text(error_msg)
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Exception while handling an update: {context.error}")
        
        if isinstance(update, Update) and update.effective_message:
            try:
                user_lang = self.language_handler.detect_user_language(
                    update.effective_user.language_code if update.effective_user else None
                )
                error_msg = self.language_handler.get_message("error", user_lang)
                await update.effective_message.reply_text(error_msg)
            except Exception as e:
                logger.error(f"Error sending error message: {e}")
