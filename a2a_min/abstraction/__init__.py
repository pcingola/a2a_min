"""A2A Min abstraction layer.

This module provides a simplified abstraction layer for the A2A Min client-server architecture.
"""

from a2a_min.abstraction.agent import AgentAdapter
from a2a_min.abstraction.client import A2aMinClient
from a2a_min.abstraction.server import A2aMinServer, Middleware
from a2a_min.abstraction.middleware import LoggingMiddleware, MetricsMiddleware, DebugMiddleware
from a2a_min.abstraction.types import AgentInvocationResult, TaskUpdate

__all__ = [
    "AgentAdapter",
    "A2aMinClient",
    "A2aMinServer",
    "Middleware",
    "LoggingMiddleware",
    "MetricsMiddleware",
    "DebugMiddleware",
    "AgentInvocationResult",
    "TaskUpdate",
]