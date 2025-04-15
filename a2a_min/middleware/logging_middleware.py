"""Middleware implementations for the A2A Min abstraction layer."""

import logging
from typing import Any

class LoggingMiddleware:
    """Middleware for logging requests and responses."""
    
    def __init__(self, logger: logging.Logger | None = None):
        """Initialize the middleware.
        
        Args:
            logger: The logger to use. If not provided, a new one will be created.
        """
        self.logger = logger or logging.getLogger(__name__)
    
    async def process_request(self, request: Any) -> Any:
        """Log the request and pass it through.
        
        Args:
            request: The request to log.
            
        Returns:
            The request, unchanged.
        """
        self.logger.info(f"Request: {request}")
        return request
    
    async def process_response(self, response: Any) -> Any:
        """Log the response and pass it through.
        
        Args:
            response: The response to log.
            
        Returns:
            The response, unchanged.
        """
        self.logger.info(f"Response: {response}")
        return response
