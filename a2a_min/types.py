"""Types for the A2A Min abstraction layer."""

from typing import Any
from pydantic import BaseModel
from a2a_min.base.types import Message, TaskState, Artifact, TextPart


class AgentInvocationResult(BaseModel):
    """Result of an agent invocation."""
    message: Message
    is_complete: bool = True
    requires_input: bool = False
    metadata: dict[str, Any] | None = None
    
    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def agent_msg(cls, message: str):
        return cls(message=Message(
            role="agent",
            parts=[TextPart(text=message)]
        ))


class TaskUpdate(BaseModel):
    """An update from a streaming task."""
    status: TaskState | None = None
    artifact: Artifact | None = None
    is_final: bool = False
    metadata: dict[str, Any] | None = None

    class Config:
        arbitrary_types_allowed = True
