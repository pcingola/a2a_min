
from typing import Any


class Middleware:
    """Base class for middleware."""
    
    async def process_request(self, request: Any) -> Any:
        """Process a request before it's handled by the server.
        
        Args:
            request: The request to process.
            
        Returns:
            The processed request.
        """
        return request
    
    async def process_response(self, response: Any) -> Any:
        """Process a response before it's sent to the client.
        
        Args:
            response: The response to process.
            
        Returns:
            The processed response.
        """
        return response