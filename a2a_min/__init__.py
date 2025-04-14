"""
A2A-min: Agent to Agent (A2A) minimalistic Python SDK

This package provides a minimalistic SDK for agent-to-agent communication.
"""

__version__ = "0.1.0"

# Import key types
from a2a_min.types import (
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

# Import client
from a2a_min.client.client import A2AClient
from a2a_min.client.card_resolver import A2ACardResolver

# Import server
from a2a_min.server.server import A2AServer
from a2a_min.server.task_manager import TaskManager

# Import exceptions
from a2a_min.types import (
    A2AClientError,
    A2AClientHTTPError,
    A2AClientJSONError,
    MissingAPIKeyError,
)
