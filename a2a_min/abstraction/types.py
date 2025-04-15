"""Types for the A2A Min abstraction layer."""

from pydantic import BaseModel
from a2a_min.base.types import Message, TaskState, Artifact


class AgentInvocationResult(BaseModel):
    """Result of an agent invocation."""
    message: Message
    is_complete: bool = True
    requires_input: bool = False
    metadata: dict[str, any] | None = None
    
    class Config:
        arbitrary_types_allowed = True


class TaskUpdate(BaseModel):
    """An update from a streaming task."""
    status: TaskState | None = None
    artifact: Artifact | None = None
    is_final: bool = False
    metadata: dict[str, any] | None = None

    class Config:
        arbitrary_types_allowed = True
