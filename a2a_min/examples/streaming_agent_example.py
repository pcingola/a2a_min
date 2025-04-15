"""Example of using the A2A Min abstraction layer with a streaming agent."""

import asyncio
from a2a_min import (
    AgentAdapter,
    A2aMinServer,
    A2aMinClient,
    AgentInvocationResult,
    LoggingMiddleware,
)
from a2a_min.base.types import Message, TextPart
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StreamingAgent(AgentAdapter):
    """A simple agent that streams its response word by word."""
    
    @property
    def name(self) -> str:
        return "Streaming Agent"
    
    @property
    def description(self) -> str:
        return "An agent that streams its response word by word"
    
    @property
    def capabilities(self):
        capabilities = super().capabilities
        capabilities.streaming = True
        return capabilities
    
    def invoke(self, query: str, session_id: str) -> AgentInvocationResult:
        """Generate a response to the query."""
        response = f"You asked: {query}. This is a non-streaming response."
        return AgentInvocationResult(
            message=Message(
                role="agent",
                parts=[TextPart(text=response)]
            ),
            is_complete=True,
            requires_input=False
        )
    
    async def stream(self, query: str, session_id: str):
        """Stream a response word by word."""
        # Generate a response
        words = f"You asked: {query}. This is a streaming response that comes word by word.".split()
        
        # Stream partial responses
        for i, word in enumerate(words):
            # Create a partial response with the words so far
            partial_text = " ".join(words[:i+1])
            
            # Yield a partial response
            yield AgentInvocationResult(
                message=Message(
                    role="agent",
                    parts=[TextPart(text=partial_text)]
                ),
                is_complete=False,
                requires_input=False
            )
            
            # Simulate some processing time
            await asyncio.sleep(0.2)
        
        # Yield the final response
        yield AgentInvocationResult(
            message=Message(
                role="agent",
                parts=[TextPart(text=" ".join(words))]
            ),
            is_complete=True,
            requires_input=False
        )

async def run_client(url: str):
    """Run a client that sends a message to the streaming agent."""
    client = A2aMinClient.connect(url)
    
    print("Sending a regular (non-streaming) message...")
    task = await client.send_message("Hello, Streaming Agent!")
    
    # Print the response
    for artifact in task.artifacts:
        for part in artifact.parts:
            if hasattr(part, "text"):
                print(f"Regular response: {part.text}")
    
    print("\nSending a streaming message...")
    async for update in client.send_message_streaming("Tell me a story"):
        if update.artifact:
            for part in update.artifact.parts:
                if hasattr(part, "text"):
                    print(f"\rStreaming response: {part.text}", end="")
        if update.is_final:
            print()  # Add a newline at the end

def start_server():
    """Start the streaming agent server."""
    # Create the agent
    agent = StreamingAgent()
    
    # Create middleware
    logging_middleware = LoggingMiddleware()
    
    # Create and start the server
    server = A2aMinServer.from_agent(
        agent,
        host="localhost",
        port=8001,
        middlewares=[logging_middleware]
    )
    
    logger.info("Starting Streaming Agent server on http://localhost:8001")
    server.start()

async def main():
    """Run the example."""
    # In a real application, you would run the server in a separate process
    # For this example, we'll just run the client
    await run_client("http://localhost:8001")

if __name__ == "__main__":
    # To run this example:
    # 1. Start the server in one terminal: python -m a2a_min.examples.streaming_agent_example server
    # 2. Run the client in another terminal: python -m a2a_min.examples.streaming_agent_example client
    
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "server":
            start_server()
        elif sys.argv[1] == "client":
            asyncio.run(main())
        else:
            print("Usage: python -m a2a_min.examples.streaming_agent_example [server|client]")
    else:
        print("Usage: python -m a2a_min.examples.streaming_agent_example [server|client]")