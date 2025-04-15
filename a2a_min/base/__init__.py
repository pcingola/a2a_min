"""
A2A-min: Agent to Agent (A2A) minimalistic Python SDK

This package provides a minimalistic SDK for agent-to-agent communication.
"""

__version__ = "0.1.0"

# Import key types
from a2a_min.base.types import (
    AgentCard,
    AgentProvider,
    AgentCapabilities,
    AgentAuthentication,
    AgentSkill,
    Task,
    TaskState,
    Message,
    TextPart,
    FilePart,
    DataPart,
    Part,
    TaskStatus,
    Artifact,
    PushNotificationConfig,
)

# Import exceptions
from a2a_min.base.types import (
    A2AClientError,
    A2AClientHTTPError,
    A2AClientJSONError,
    MissingAPIKeyError,
)
