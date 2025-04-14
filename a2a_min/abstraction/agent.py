"""Base agent interface for the A2A Min abstraction layer."""

from abc import ABC, abstractmethod
from typing import AsyncIterable, List, Optional, Dict, Any
from a2a_min.types import AgentCard, AgentCapabilities, AgentSkill, Message, Part, TextPart
from a2a_min.abstraction.types import AgentInvocationResult

class BaseAgent(ABC):
    """Base class for all agents.
    
    This class defines the interface that all agents must implement.
    """
    
    @property
    def name(self) -> str:
        """Return the name of the agent."""
        return self.__class__.__name__
    
    @property
    def description(self) -> str:
        """Return a description of the agent."""
        return "A generic agent"
    
    @property
    def supported_content_types(self) -> List[str]:
        """Return the content types supported by this agent."""
        return ["text"]
    
    @property
    def capabilities(self) -> AgentCapabilities:
        """Return the capabilities of this agent."""
        return AgentCapabilities(
            streaming=hasattr(self, "stream") and callable(getattr(self, "stream")),
            pushNotifications=False,
            stateTransitionHistory=False
        )
    
    @property
    def skills(self) -> List[AgentSkill]:
        """Return the skills of this agent."""
        return [
            AgentSkill(
                id=f"{self.name.lower()}_skill",
                name=self.name,
                description=self.description,
                tags=[],
                examples=[]
            )
        ]
    
    def get_agent_card(self, url: str = "http://localhost:8000/") -> AgentCard:
        """Generate an agent card for this agent.
        
        Args:
            url: The URL where the agent is hosted.
            
        Returns:
            An AgentCard instance describing this agent.
        """
        return AgentCard(
            name=self.name,
            description=self.description,
            url=url,
            version="1.0.0",
            capabilities=self.capabilities,
            skills=self.skills,
            defaultInputModes=self.supported_content_types,
            defaultOutputModes=self.supported_content_types
        )
    
    @abstractmethod
    def invoke(self, query: str, session_id: str) -> AgentInvocationResult:
        """Synchronously process a query and return a response.
        
        Args:
            query: The user's query.
            session_id: A unique identifier for the session.
            
        Returns:
            An AgentInvocationResult containing the agent's response.
        """
        pass
    
    async def stream(self, query: str, session_id: str) -> AsyncIterable[AgentInvocationResult]:
        """Stream a response to a query.
        
        Default implementation yields the invoke result.
        
        Args:
            query: The user's query.
            session_id: A unique identifier for the session.
            
        Yields:
            AgentInvocationResult objects containing parts of the agent's response.
        """
        yield self.invoke(query, session_id)