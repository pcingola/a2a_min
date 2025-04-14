"""Types for the A2A Min abstraction layer."""

from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from a2a_min.types import Message, Part, TaskState, Artifact

class AgentInvocationResult(BaseModel):
    """Result of an agent invocation."""
    message: Message
    is_complete: bool = True
    requires_input: bool = False
    metadata: Optional[Dict[str, Any]] = None

class TaskUpdate(BaseModel):
    """An update from a streaming task."""
    status: Optional[TaskState] = None
    artifact: Optional[Artifact] = None
    is_final: bool = False
    metadata: Optional[Dict[str, Any]] = None