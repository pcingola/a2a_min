"""Middleware implementations for the A2A Min abstraction layer."""

from typing import Any, Callable


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