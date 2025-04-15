""" Example of using the A2A Min abstraction layer with a simple echo client """

import asyncio
from a2a_min import A2aMinClient


async def run_client(url: str):
    """Run a client that sends a message to the echo agent."""


async def client():
    """ Run the example client """
    client = A2aMinClient.connect("http://localhost:8000")
    task = await client.send_message("Hello, Echo Agent!")    
    # Print the response
    for artifact in task.artifacts:
        for part in artifact.parts:
            if hasattr(part, "text"):
                print(f"Response: {part.text}")


if __name__ == "__main__":
    # Run the client
    asyncio.run(client())
