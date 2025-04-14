"""Middleware implementations for the A2A Min abstraction layer."""

import logging
import time
from typing import Any, Callable, Optional

class LoggingMiddleware:
    """Middleware for logging requests and responses."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
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

class MetricsMiddleware:
    """Middleware for collecting metrics."""
    
    def __init__(self, metrics_callback: Callable[[str, float], None]):
        """Initialize the middleware.
        
        Args:
            metrics_callback: A callback function that will be called with the metric name and value.
        """
        self.metrics_callback = metrics_callback
        self.start_times = {}
    
    async def process_request(self, request: Any) -> Any:
        """Start timing the request.
        
        Args:
            request: The request to time.
            
        Returns:
            The request, unchanged.
        """
        request_id = id(request)
        self.start_times[request_id] = time.time()
        return request
    
    async def process_response(self, response: Any) -> Any:
        """Record the time taken to process the request.
        
        Args:
            response: The response to the request.
            
        Returns:
            The response, unchanged.
        """
        request_id = id(response)
        if request_id in self.start_times:
            elapsed = time.time() - self.start_times[request_id]
            self.metrics_callback("request_time", elapsed)
            del self.start_times[request_id]
        return response

class DebugMiddleware:
    """Middleware for debugging requests and responses."""
    
    def __init__(self, debug_callback: Callable[[str, Any], None]):
        """Initialize the middleware.
        
        Args:
            debug_callback: A callback function that will be called with the event name and data.
        """
        self.debug_callback = debug_callback
    
    async def process_request(self, request: Any) -> Any:
        """Debug the request.
        
        Args:
            request: The request to debug.
            
        Returns:
            The request, unchanged.
        """
        self.debug_callback("request", request)
        return request
    
    async def process_response(self, response: Any) -> Any:
        """Debug the response.
        
        Args:
            response: The response to debug.
            
        Returns:
            The response, unchanged.
        """
        self.debug_callback("response", response)
        return response