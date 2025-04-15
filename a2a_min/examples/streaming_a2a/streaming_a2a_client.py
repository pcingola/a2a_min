"""Example of using the A2A Min abstraction layer with a streaming client."""

import asyncio
from a2a_min import A2aMinClient
from a2a_min.base.types import TaskStatusUpdateEvent


async def run_client(url: str = "http://localhost:8000"):
    """Run a client that sends a message to the streaming agent."""
    client = A2aMinClient.connect(url)
    async for update in client.send_message_streaming("Tell me a story"):
        res = update.result
        if isinstance(res, TaskStatusUpdateEvent):
            print(res.status.message.parts[0].text, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(run_client())
