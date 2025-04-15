"""Middleware implementations for the A2A Min abstraction layer."""

import time
from typing import Any, Callable

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
