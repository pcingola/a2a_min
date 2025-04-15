"""Example of using the A2A Min abstraction layer with a multimodal agent."""

import asyncio
from a2a_min import (
    AgentAdapter,
    A2aMinServer,
    A2aMinClient,
    AgentInvocationResult,
    LoggingMiddleware,
)
from a2a_min.base.types import Message, TextPart, FilePart, FileContent, DataPart
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiModalAgent(AgentAdapter):
    """An agent that can respond with different content types."""
    
    @property
    def name(self) -> str:
        return "MultiModal Agent"
    
    @property
    def description(self) -> str:
        return "An agent that can respond with text, images, and structured data"
    
    @property
    def supported_content_types(self) -> list:
        return ["text", "file", "data"]
    
    def invoke(self, query: str, session_id: str) -> AgentInvocationResult:
        """Generate a response based on the query."""
        query_lower = query.lower()
        
        # Text response
        if "text" in query_lower:
            return AgentInvocationResult(
                message=Message(
                    role="agent",
                    parts=[TextPart(text="This is a text response")]
                ),
                is_complete=True,
                requires_input=False
            )
        
        # Image response
        elif "image" in query_lower:
            return AgentInvocationResult(
                message=Message(
                    role="agent",
                    parts=[
                        TextPart(text="Here's an image:"),
                        FilePart(
                            file=FileContent(
                                name="example.jpg",
                                mimeType="image/jpeg",
                                uri="https://example.com/image.jpg"
                            )
                        )
                    ]
                ),
                is_complete=True,
                requires_input=False
            )
        
        # Data response
        elif "data" in query_lower:
            return AgentInvocationResult(
                message=Message(
                    role="agent",
                    parts=[
                        TextPart(text="Here's some structured data:"),
                        DataPart(
                            data={
                                "name": "John Doe",
                                "age": 30,
                                "occupation": "Software Engineer",
                                "skills": ["Python", "JavaScript", "Machine Learning"]
                            }
                        )
                    ]
                ),
                is_complete=True,
                requires_input=False
            )
        
        # Mixed response
        else:
            return AgentInvocationResult(
                message=Message(
                    role="agent",
                    parts=[
                        TextPart(text="This is a mixed response with text, an image, and data."),
                        FilePart(
                            file=FileContent(
                                name="example.jpg",
                                mimeType="image/jpeg",
                                uri="https://example.com/image.jpg"
                            )
                        ),
                        DataPart(
                            data={
                                "temperature": 72.5,
                                "unit": "Fahrenheit",
                                "conditions": "Sunny"
                            }
                        )
                    ]
                ),
                is_complete=True,
                requires_input=False
            )

async def run_client(url: str):
    """Run a client that sends messages to the multimodal agent."""
    client = A2aMinClient.connect(url)
    
    # Test text response
    print("Requesting a text response...")
    task = await client.send_message("Give me some text")
    print_response(task)
    
    # Test image response
    print("\nRequesting an image response...")
    task = await client.send_message("Show me an image")
    print_response(task)
    
    # Test data response
    print("\nRequesting a data response...")
    task = await client.send_message("Give me some data")
    print_response(task)
    
    # Test mixed response
    print("\nRequesting a mixed response...")
    task = await client.send_message("Give me a mixed response")
    print_response(task)

def print_response(task):
    """Print the response from the agent."""
    if task.artifacts:
        for artifact in task.artifacts:
            for part in artifact.parts:
                if hasattr(part, "text"):
                    print(f"Text: {part.text}")
                elif hasattr(part, "file"):
                    print(f"File: {part.file.name} ({part.file.mimeType})")
                    if part.file.uri:
                        print(f"  URI: {part.file.uri}")
                elif hasattr(part, "data"):
                    print(f"Data: {json.dumps(part.data, indent=2)}")

def start_server():
    """Start the multimodal agent server."""
    # Create the agent
    agent = MultiModalAgent()
    
    # Create middleware
    logging_middleware = LoggingMiddleware()
    
    # Create and start the server
    server = A2aMinServer.from_agent(
        agent,
        host="localhost",
        port=8002,
        middlewares=[logging_middleware]
    )
    
    logger.info("Starting MultiModal Agent server on http://localhost:8002")
    server.start()

async def main():
    """Run the example."""
    # In a real application, you would run the server in a separate process
    # For this example, we'll just run the client
    await run_client("http://localhost:8002")

if __name__ == "__main__":
    # To run this example:
    # 1. Start the server in one terminal: python -m a2a_min.examples.multimodal_agent_example server
    # 2. Run the client in another terminal: python -m a2a_min.examples.multimodal_agent_example client
    
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "server":
            start_server()
        elif sys.argv[1] == "client":
            asyncio.run(main())
        else:
            print("Usage: python -m a2a_min.examples.multimodal_agent_example [server|client]")
    else:
        print("Usage: python -m a2a_min.examples.multimodal_agent_example [server|client]")