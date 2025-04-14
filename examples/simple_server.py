#!/usr/bin/env python3
"""
Simple example of creating an A2A server.

This script demonstrates how to create and run an A2A server that can handle tasks.
"""

import asyncio
from a2a_min import (
    A2AServer,
    TaskManager,
    AgentCard,
    AgentProvider,
    AgentCapabilities,
    AgentSkill,
    TaskState,
    JSONRPCResponse,
    Task,
    TaskStatus,
    TextPart,
    Message,
)
from a2a_min.types import SendTaskRequest
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server configuration
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "5000"))


class SimpleTaskManager(TaskManager):
    """A simple task manager that processes tasks."""
    
    async def on_send_task(self, request: SendTaskRequest) -> JSONRPCResponse:
        """Handle a task request."""
        logger.info(f"Received task: {request.params.id}")
        
        # Extract the message from the request
        message = request.params.message
        
        # Process the message (in a real application, this would do something useful)
        response_text = f"Processed task {request.params.id}"
        
        # Create a response message
        response_message = Message(
            role="agent",
            parts=[TextPart(text=response_text)]
        )
        
        # Create a task status
        task_status = TaskStatus(
            state=TaskState.COMPLETED,
            message=response_message
        )
        
        # Create a task
        task = Task(
            id=request.params.id,
            sessionId=request.params.sessionId,
            status=task_status,
            history=[Message(**message)]
        )
        
        # Return the response
        return JSONRPCResponse(
            id=request.id,
            result=task
        )


def main():
    # Create an agent card
    agent_card = AgentCard(
        name="Simple A2A Agent",
        description="A simple A2A agent example",
        url=f"http://{HOST}:{PORT}",
        provider=AgentProvider(
            organization="Example Org",
            url="https://example.org"
        ),
        version="1.0.0",
        capabilities=AgentCapabilities(
            streaming=False,
            pushNotifications=False,
            stateTransitionHistory=False
        ),
        skills=[
            AgentSkill(
                id="example",
                name="Example Skill",
                description="An example skill that processes tasks"
            )
        ]
    )
    
    # Create a task manager
    task_manager = SimpleTaskManager()
    
    # Create and start the server
    server = A2AServer(
        host=HOST,
        port=PORT,
        agent_card=agent_card,
        task_manager=task_manager
    )
    
    logger.info(f"Starting server on {HOST}:{PORT}")
    server.start()


if __name__ == "__main__":
    main()