"""Task manager implementation for the A2A Min abstraction layer."""

from typing import AsyncIterable, Union
from a2a_min.base.server.task_manager import InMemoryTaskManager
from a2a_min.base.types import (
    SendTaskRequest, SendTaskResponse, SendTaskStreamingRequest,
    JSONRPCResponse, TaskStatus, TaskState, Message, Artifact,
    TextPart, TaskStatusUpdateEvent, TaskArtifactUpdateEvent
)
from a2a_min.agent_adapter import AgentAdapter
import asyncio
import logging


logger = logging.getLogger(__name__)


class A2aMinTaskManager(InMemoryTaskManager):
    """A simplified task manager for A2A servers."""
    
    def __init__(self, agent: AgentAdapter):
        """Initialize the task manager.
        
        Args:
            agent: The agent to use for processing tasks.
        """
        super().__init__()
        self.agent = agent
    
    async def on_send_task(self, request: SendTaskRequest) -> SendTaskResponse:
        """Handle a send task request.
        
        Args:
            request: The send task request.
            
        Returns:
            A response containing the result of the task.
        """
        await self.upsert_task(request.params)
        task = await self.update_store(
            request.params.id, TaskStatus(state=TaskState.WORKING), None
        )
        
        query = self._get_user_query(request.params)
        
        try:
            agent_result = self.agent.invoke(query, request.params.sessionId)
            
            artifact = None
            task_status = None
            
            if agent_result.requires_input:
                task_status = TaskStatus(
                    state=TaskState.INPUT_REQUIRED,
                    message=agent_result.message
                )
            else:
                task_status = TaskStatus(state=TaskState.COMPLETED)
                artifact = Artifact(parts=agent_result.message.parts)
            
            task = await self.update_store(
                request.params.id, task_status, None if artifact is None else [artifact]
            )
            
            task_result = self.append_task_history(task, request.params.historyLength)
            return SendTaskResponse(id=request.id, result=task_result)
            
        except Exception as e:
            logger.error(f"Error invoking agent: {e}")
            raise ValueError(f"Error invoking agent: {e}")
    
    async def on_send_task_subscribe(
        self, request: SendTaskStreamingRequest
    ) -> Union[AsyncIterable[JSONRPCResponse], JSONRPCResponse]:
        """Handle a streaming send task request.
        
        Args:
            request: The streaming send task request.
            
        Returns:
            An async iterable of responses or an error response.
        """
        await self.upsert_task(request.params)
        sse_event_queue = await self.setup_sse_consumer(request.params.id, False)
        
        asyncio.create_task(self._run_streaming_agent(request))
        
        return self.dequeue_events_for_sse(
            request.id, request.params.id, sse_event_queue
        )
    
    async def _run_streaming_agent(self, request: SendTaskStreamingRequest):
        """Run the agent in streaming mode.
        
        Args:
            request: The streaming send task request.
        """
        query = self._get_user_query(request.params)
        
        try:
            async for agent_result in self.agent.stream(query, request.params.sessionId):
                artifact = None
                end_stream = False
                
                if not agent_result.is_complete and not agent_result.requires_input:
                    task_state = TaskState.WORKING
                elif agent_result.requires_input:
                    task_state = TaskState.INPUT_REQUIRED
                    end_stream = True
                else:
                    task_state = TaskState.COMPLETED
                    artifact = Artifact(parts=agent_result.message.parts, index=0, append=False)
                    end_stream = True
                
                task_status = TaskStatus(state=task_state, message=agent_result.message)
                await self.update_store(
                    request.params.id,
                    task_status,
                    None if artifact is None else [artifact]
                )
                
                if artifact:
                    task_artifact_update_event = TaskArtifactUpdateEvent(
                        id=request.params.id, artifact=artifact
                    )
                    await self.enqueue_events_for_sse(
                        request.params.id, task_artifact_update_event
                    )
                
                task_update_event = TaskStatusUpdateEvent(
                    id=request.params.id, status=task_status, final=end_stream
                )
                await self.enqueue_events_for_sse(
                    request.params.id, task_update_event
                )
                
        except Exception as e:
            logger.error(f"Error in streaming agent: {e}")
            await self.enqueue_events_for_sse(
                request.params.id,
                TaskStatusUpdateEvent(
                    id=request.params.id,
                    status=TaskStatus(
                        state=TaskState.FAILED,
                        message=Message(
                            role="agent",
                            parts=[TextPart(text=f"Error: {str(e)}")]
                        )
                    ),
                    final=True
                )
            )
    
    def _get_user_query(self, task_send_params):
        """Extract the user query from the task parameters.
        
        Args:
            task_send_params: The task send parameters.
            
        Returns:
            The user query as a string.
        """
        part = task_send_params.message.parts[0]
        if not hasattr(part, "text"):
            raise ValueError("Only text parts are supported")
        return part.text