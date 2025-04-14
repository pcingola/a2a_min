"""Example of using the A2A Min abstraction layer with a simple echo agent."""

import asyncio
from a2a_min import (
    BaseAgent,
    A2aMinServer,
    A2aMinClient,
    AgentInvocationResult,
    LoggingMiddleware,
    MetricsMiddleware,
)
from a2a_min.types import Message, TextPart
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EchoAgent(BaseAgent):
    """A simple echo agent that repeats the user's message."""
    
    @property
    def name(self) -> str:
        return "Echo Agent"
    
    @property
    def description(self) -> str:
        return "A simple agent that echoes back what you say"
    
    def invoke(self, query: str, session_id: str) -> AgentInvocationResult:
        """Echo back the user's query."""
        return AgentInvocationResult(
            message=Message(
                role="agent",
                parts=[TextPart(text=f"Echo: {query}")]
            ),
            is_complete=True,
            requires_input=False
        )

async def run_client(url: str):
    """Run a client that sends a message to the echo agent."""
    client = A2aMinClient.connect(url)
    
    # Send a message and get a response
    task = await client.send_message("Hello, Echo Agent!")
    
    # Print the response
    for artifact in task.artifacts:
        for part in artifact.parts:
            if hasattr(part, "text"):
                print(f"Response: {part.text}")

def record_metric(name, value):
    """Record a metric."""
    logger.info(f"Metric {name}: {value}")

def start_server():
    """Start the echo agent server."""
    # Create the agent
    agent = EchoAgent()
    
    # Create middleware
    logging_middleware = LoggingMiddleware()
    metrics_middleware = MetricsMiddleware(record_metric)
    
    # Create and start the server
    server = A2aMinServer.from_agent(
        agent,
        host="localhost",
        port=8000,
        middlewares=[logging_middleware, metrics_middleware]
    )
    
    logger.info("Starting Echo Agent server on http://localhost:8000")
    server.start()

async def main():
    """Run the example."""
    # In a real application, you would run the server in a separate process
    # For this example, we'll just run the client
    await run_client("http://localhost:8000")

if __name__ == "__main__":
    # To run this example:
    # 1. Start the server in one terminal: python -m a2a_min.examples.echo_agent_example server
    # 2. Run the client in another terminal: python -m a2a_min.examples.echo_agent_example client
    
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "server":
            start_server()
        elif sys.argv[1] == "client":
            asyncio.run(main())
        else:
            print("Usage: python -m a2a_min.examples.echo_agent_example [server|client]")
    else:
        print("Usage: python -m a2a_min.examples.echo_agent_example [server|client]")