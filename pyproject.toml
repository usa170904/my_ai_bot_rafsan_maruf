"""
Utility functions for the Telegram bot
"""

import re
import logging
from typing import List

logger = logging.getLogger(__name__)

def format_code_response(response: str) -> str:
    """
    Format code response with proper markdown formatting
    
    Args:
        response: Raw response from Gemini
        
    Returns:
        Formatted response with code blocks
    """
    try:
        # If the response already contains code blocks, return as is
        if "```" in response:
            return response
        
        # Try to detect code patterns and wrap them in code blocks
        lines = response.split('\n')
        formatted_lines = []
        in_code_block = False
        current_language = ""
        
        for line in lines:
            # Check for common code indicators
            if _is_code_line(line) and not in_code_block:
                # Start a code block
                current_language = _detect_language(line)
                formatted_lines.append(f"```{current_language}")
                formatted_lines.append(line)
                in_code_block = True
            elif in_code_block and (line.strip() == "" or _is_code_line(line)):
                # Continue code block
                formatted_lines.append(line)
            elif in_code_block and not _is_code_line(line):
                # End code block
                formatted_lines.append("```")
                formatted_lines.append("")
                formatted_lines.append(line)
                in_code_block = False
            else:
                # Regular text
                formatted_lines.append(line)
        
        # Close any open code block
        if in_code_block:
            formatted_lines.append("```")
        
        return '\n'.join(formatted_lines)
        
    except Exception as e:
        logger.error(f"Error formatting code response: {e}")
        return response

def _is_code_line(line: str) -> bool:
    """Check if a line looks like code"""
    line = line.strip()
    
    if not line:
        return False
    
    # Common code patterns
    code_patterns = [
        r'^(def|class|function|var|let|const|import|from|#include)',  # Function/class/import declarations
        r'^[a-zA-Z_][a-zA-Z0-9_]*\s*=',  # Variable assignments
        r'^\s*(if|for|while|try|catch|switch|case)',  # Control structures
        r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\(',  # Function calls
        r'[{};]$',  # Code line endings
        r'^\s*[<>]\w+',  # HTML tags
        r'^\s*\.|^\s*#|^\s*//',  # CSS, comments
        r'console\.|print\(|echo\s',  # Output statements
    ]
    
    for pattern in code_patterns:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    
    return False

def _detect_language(line: str) -> str:
    """Detect programming language from a code line"""
    line_lower = line.lower().strip()
    
    # Language detection patterns
    if 'def ' in line_lower or 'import ' in line_lower or 'print(' in line_lower:
        return 'python'
    elif 'function' in line_lower or 'const ' in line_lower or 'let ' in line_lower:
        return 'javascript'
    elif '#include' in line_lower or 'cout <<' in line_lower:
        return 'cpp'
    elif 'public class' in line_lower or 'System.out' in line_lower:
        return 'java'
    elif '<html>' in line_lower or '<!DOCTYPE' in line_lower:
        return 'html'
    elif 'body {' in line_lower or '.class' in line_lower:
        return 'css'
    elif 'SELECT' in line_lower or 'INSERT' in line_lower:
        return 'sql'
    elif '#!/bin/bash' in line_lower or 'echo ' in line_lower:
        return 'bash'
    
    return ''

def escape_markdown(text: str) -> str:
    """
    Escape special characters for Telegram markdown V2
    
    Args:
        text: Text to escape
        
    Returns:
        Escaped text safe for markdown
    """
    # Characters that need escaping in Telegram MarkdownV2
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!', '\\']
    
    # First escape backslashes
    text = text.replace('\\', '\\\\')
    
    # Then escape other characters
    for char in escape_chars[:-1]:  # Skip backslash as it's already done
        text = text.replace(char, f'\\{char}')
    
    return text

def split_long_message(message: str, max_length: int = 4096) -> List[str]:
    """
    Split long messages into chunks that fit Telegram's limits
    
    Args:
        message: Message to split
        max_length: Maximum length per chunk
        
    Returns:
        List of message chunks
    """
    if len(message) <= max_length:
        return [message]
    
    chunks = []
    lines = message.split('\n')
    current_chunk = ""
    
    for line in lines:
        # If adding this line would exceed the limit
        if len(current_chunk) + len(line) + 1 > max_length:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = line + '\n'
            else:
                # Line is too long, split it further
                while len(line) > max_length:
                    chunks.append(line[:max_length])
                    line = line[max_length:]
                current_chunk = line + '\n' if line else ""
        else:
            current_chunk += line + '\n'
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def clean_code_response(response: str) -> str:
    """
    Clean and format code response from Gemini
    
    Args:
        response: Raw response from Gemini
        
    Returns:
        Cleaned response
    """
    # Remove any leading/trailing whitespace
    response = response.strip()
    
    # Fix common formatting issues
    response = response.replace('```python\n\n', '```python\n')
    response = response.replace('\n\n```', '\n```')
    
    # Ensure proper spacing around code blocks
    response = re.sub(r'```(\w+)', r'\n```\1', response)
    response = re.sub(r'```\n\n', r'```\n', response)
    
    return response

def log_user_interaction(user_id: int, username: str, message_type: str, message_length: int):
    """
    Log user interactions for monitoring and debugging
    
    Args:
        user_id: Telegram user ID
        username: Telegram username
        message_type: Type of message (code, question, etc.)
        message_length: Length of the message
    """
    logger.info(f"User interaction - ID: {user_id}, Username: {username}, "
                f"Type: {message_type}, Length: {message_length}")
