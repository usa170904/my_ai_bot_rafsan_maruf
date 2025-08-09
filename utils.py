# Overview

This is an advanced multilingual Telegram bot powered by Google Gemini 2.5 Flash AI that provides comprehensive coding assistance, AI/ML development, mobile app creation, API development, database design, and intelligent question answering in both English and Bengali. The bot serves as a complete software development assistant capable of generating production-ready code for any programming language, framework, or technology stack. It features sophisticated rate limiting, multilingual support with automatic language detection, and specialized commands for different development domains.

# User Preferences

Preferred communication style: Simple, everyday language.

**Bot Creator Information**: The bot should identify its creator as "Rafsan Maruf" when asked about who developed or created it.

# System Architecture

## Core Components

**Bot Framework**: Built using python-telegram-bot library for handling Telegram API interactions, with asyncio for asynchronous operations and proper message handling.

**AI Integration**: Advanced integration with Google Gemini 2.5 Flash model through the official genai client library providing:
- Multi-domain code generation (Python, JavaScript, Java, C++, Go, Rust, etc.)
- Full-stack development assistance (frontend, backend, databases)
- AI/ML project development with complete pipelines
- Mobile app development for iOS/Android
- API design and microservices architecture
- Intelligent question answering across all knowledge domains
- Context-aware programming assistance with best practices

**Multilingual Support**: Implements language detection using Unicode character ranges and regex patterns to automatically detect Bengali vs English input, with predefined message templates in both languages.

**Rate Limiting**: Custom rate limiter implementation using deque data structures to track user request timestamps and enforce API usage limits (default: 10 requests per 60 seconds per user).

**Command System**: Comprehensive modular command handling architecture with specialized handlers for different development domains:
- `/code` - General code generation and programming assistance
- `/app` - Desktop/mobile application development
- `/web` - Website and web application creation
- `/ai` - Artificial Intelligence and machine learning projects
- `/ml` - Dedicated machine learning model development
- `/mobile` - Cross-platform mobile app development (Flutter, React Native)
- `/api` - RESTful API and microservices development
- `/db` - Database design, optimization, and management
- `/ask` - Intelligent question answering on any topic
- `/lang` - Language detection and switching
- `/status` - Bot status and capabilities information

## Design Patterns

**Configuration Management**: Centralized configuration system using environment variables with validation and fallback defaults for all bot settings including API keys, rate limits, and timeouts.

**Error Handling**: Comprehensive error handling with logging throughout all components, graceful fallbacks for API failures, and multilingual error messages.

**Modular Architecture**: Clean separation of concerns with dedicated modules for:
- Bot orchestration (bot.py)
- Command processing (commands.py)
- AI client interaction (gemini_client.py)
- Language handling (language_handler.py)
- Rate limiting (rate_limiter.py)
- Utility functions (utils.py)

**Message Processing**: Intelligent message formatting with automatic code block detection, markdown escaping, and response length management to comply with Telegram's message limits.

# External Dependencies

**Telegram Bot API**: Primary interface for receiving and sending messages through the official Telegram Bot API using python-telegram-bot library.

**Google Gemini API**: Core AI functionality provided by Google's Gemini 2.5 Flash model accessed through the official genai Python client library for text generation and code assistance.

**Environment Configuration**: Relies on environment variables for sensitive configuration:
- `TELEGRAM_BOT_TOKEN` - Telegram bot authentication
- `GEMINI_API_KEY` - Google Gemini API access
- Optional rate limiting and logging configuration variables

**Python Standard Library**: Utilizes asyncio for asynchronous operations, logging for monitoring and debugging, re for language detection patterns, and collections for rate limiting data structures.
