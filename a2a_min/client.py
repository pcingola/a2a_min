"""Client implementation for the A2A Min abstraction layer."""

from typing import AsyncIterable, Optional, List
from uuid import uuid4
from a2a_min.base.types import (
    AgentCard, Task, Message, TextPart, 
    TaskSendParams, TaskQueryParams
)
from a2a_min.base.client.card_resolver import A2ACardResolver
from a2a_min.base.client.client import A2AClient
from a2a_min.types import TaskUpdate


class A2aMinClient:
    """A simplified client for interacting with A2A servers."""
    
    def __init__(self, client: A2AClient):
        """Initialize the client.
        
        Args:
            client: The underlying A2AClient instance.
        """
        self._client = client
    
    @classmethod
    def connect(cls, url: str) -> "A2aMinClient":
        """Connect to an A2A server at the given URL.
        
        Args:
            url: The URL of the A2A server.
            
        Returns:
            An A2aMinClient instance connected to the server.
        """
        resolver = A2ACardResolver(url)
        card = resolver.get_agent_card()
        return cls.from_agent_card(card)
    
    @classmethod
    def from_agent_card(cls, card: AgentCard) -> "A2aMinClient":
        """Create a client from an agent card.
        
        Args:
            card: The agent card describing the server.
            
        Returns:
            An A2aMinClient instance configured with the agent card.
        """
        client = A2AClient(agent_card=card)
        return cls(client)
    
    async def send_message(
        self, 
        message: str, 
        session_id: Optional[str] = None,
        task_id: Optional[str] = None,
        accepted_output_modes: Optional[List[str]] = None
    ) -> Task:
        """Send a message to the agent and get a response.
        
        Args:
            message: The message to send.
            session_id: An optional session ID. If not provided, a new one will be generated.
            task_id: An optional task ID. If not provided, a new one will be generated.
            accepted_output_modes: Optional list of accepted output modes.
            
        Returns:
            A Task object containing the agent's response.
        """
        if session_id is None:
            session_id = uuid4().hex
        
        if task_id is None:
            task_id = uuid4().hex
        
        if accepted_output_modes is None:
            accepted_output_modes = ["text"]
        
        message_obj = Message(
            role="user", 
            parts=[TextPart(text=message)]
        )
        
        params = TaskSendParams(
            id=task_id,
            sessionId=session_id,
            message=message_obj,
            acceptedOutputModes=accepted_output_modes
        )
        
        response = await self._client.send_task(params)
        return response.result
    
    async def send_message_streaming(
        self, 
        message: str, 
        session_id: Optional[str] = None,
        task_id: Optional[str] = None,
        accepted_output_modes: Optional[List[str]] = None
    ) -> AsyncIterable[TaskUpdate]:
        """Send a message to the agent and get a streaming response.
        
        Args:
            message: The message to send.
            session_id: An optional session ID. If not provided, a new one will be generated.
            task_id: An optional task ID. If not provided, a new one will be generated.
            accepted_output_modes: Optional list of accepted output modes.
            
        Yields:
            TaskUpdate objects containing parts of the agent's response.
        """
        if session_id is None:
            session_id = uuid4().hex
        
        if task_id is None:
            task_id = uuid4().hex
        
        if accepted_output_modes is None:
            accepted_output_modes = ["text"]
        
        message_obj = Message(
            role="user", 
            parts=[TextPart(text=message)]
        )
        
        params = TaskSendParams(
            id=task_id,
            sessionId=session_id,
            message=message_obj,
            acceptedOutputModes=accepted_output_modes
        )
        
        async for update in self._client.send_task_streaming(params):
            if hasattr(update.result, "status"):
                status_update = update.result
                yield TaskUpdate(
                    status=status_update.status.state,
                    is_final=status_update.final,
                    metadata=status_update.metadata
                )
            elif hasattr(update.result, "artifact"):
                artifact_update = update.result
                yield TaskUpdate(
                    artifact=artifact_update.artifact,
                    metadata=artifact_update.metadata
                )
    
    async def get_task(self, task_id: str, history_length: Optional[int] = None) -> Task:
        """Get a task by ID.
        
        Args:
            task_id: The ID of the task to get.
            history_length: The maximum number of history items to include.
            
        Returns:
            The task with the given ID.
        """
        params = TaskQueryParams(
            id=task_id,
            historyLength=history_length
        )
        
        response = await self._client.get_task(params)
        return response.result