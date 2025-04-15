#!/usr/bin/env python3
"""
Simple example of using the A2A client.

This script demonstrates how to create a client and send a task to an A2A agent.
"""

import asyncio
import os
from a2a_min.base.client import A2AClient
from a2a_min.base.types import TextPart, Message, TaskState

# Replace with your agent URL
AGENT_URL = os.environ.get("AGENT_URL", "http://localhost:5000")


async def main():
    # Create a client
    client = A2AClient(url=AGENT_URL)
    
    # Create a message
    message = Message(
        role="user",
        parts=[TextPart(text="Hello, agent! Please process this task.")]
    )
    
    # Generate a unique task ID
    task_id = f"task-{asyncio.get_event_loop().time()}"
    
    print(f"Sending task {task_id} to {AGENT_URL}...")
    
    try:
        # Send a task
        response = await client.send_task({
            "id": task_id,
            "message": message.model_dump()
        })
        
        print(f"Task ID: {response.result.id}")
        print(f"Task Status: {response.result.status.state}")
        
        # If the task is not completed, poll for updates
        if response.result.status.state != TaskState.COMPLETED:
            print("Polling for task updates...")
            
            for _ in range(5):  # Poll up to 5 times
                await asyncio.sleep(1)
                
                # Get task status
                status_response = await client.get_task({"id": task_id})
                print(f"Task Status: {status_response.result.status.state}")
                
                if status_response.result.status.state in [
                    TaskState.COMPLETED, 
                    TaskState.FAILED, 
                    TaskState.CANCELED
                ]:
                    break
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())