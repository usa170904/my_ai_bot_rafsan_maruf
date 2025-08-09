"""
Rate limiting functionality to manage API usage within free tier limits
"""

import time
import logging
from collections import defaultdict, deque
from typing import Dict, Deque

logger = logging.getLogger(__name__)

class RateLimiter:
    """Simple rate limiter to prevent API abuse and stay within free tier limits"""
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        
        # Store request timestamps for each user
        self.user_requests: Dict[int, Deque[float]] = defaultdict(lambda: deque())
        
        logger.info(f"Rate limiter initialized: {max_requests} requests per {window_seconds} seconds")
    
    def check_rate_limit(self, user_id: int) -> bool:
        """
        Check if user is within rate limit
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            True if request is allowed, False if rate limited
        """
        current_time = time.time()
        user_requests = self.user_requests[user_id]
        
        # Remove old requests outside the window
        while user_requests and current_time - user_requests[0] > self.window_seconds:
            user_requests.popleft()
        
        # Check if user has exceeded the limit
        if len(user_requests) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for user {user_id}")
            return False
        
        # Add current request
        user_requests.append(current_time)
        
        return True
    
    def get_remaining_requests(self, user_id: int) -> int:
        """
        Get remaining requests for a user in the current window
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Number of remaining requests
        """
        current_time = time.time()
        user_requests = self.user_requests[user_id]
        
        # Remove old requests outside the window
        while user_requests and current_time - user_requests[0] > self.window_seconds:
            user_requests.popleft()
        
        return max(0, self.max_requests - len(user_requests))
    
    def get_reset_time(self, user_id: int) -> float:
        """
        Get time until rate limit resets for a user
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Seconds until reset, 0 if not rate limited
        """
        user_requests = self.user_requests[user_id]
        
        if not user_requests or len(user_requests) < self.max_requests:
            return 0.0
        
        oldest_request = user_requests[0]
        reset_time = oldest_request + self.window_seconds
        current_time = time.time()
        
        return max(0.0, reset_time - current_time)
    
    def cleanup_old_data(self):
        """Clean up old request data to prevent memory leaks"""
        current_time = time.time()
        users_to_remove = []
        
        for user_id, requests in self.user_requests.items():
            # Remove old requests
            while requests and current_time - requests[0] > self.window_seconds:
                requests.popleft()
            
            # If no recent requests, mark user for removal
            if not requests:
                users_to_remove.append(user_id)
        
        # Remove users with no recent requests
        for user_id in users_to_remove:
            del self.user_requests[user_id]
        
        if users_to_remove:
            logger.info(f"Cleaned up rate limit data for {len(users_to_remove)} inactive users")
