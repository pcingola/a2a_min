"""Server implementation for the A2A Min abstraction layer."""

from typing import Optional, List, Any
from a2a_min.base.server import A2AServer
from a2a_min.base.server.task_manager import TaskManager
from a2a_min.agent_adapter import AgentAdapter
from a2a_min.middleware.middleware import Middleware
from a2a_min.task_manager import A2aMinTaskManager


class A2aMinServer:
    """A simplified server for hosting A2A agents."""
    
    def __init__(
        self, 
        server: A2AServer, 
        task_manager: TaskManager,
        middlewares: Optional[List[Middleware]] = None
    ):
        """Initialize the server.
        
        Args:
            server: The underlying A2AServer instance.
            task_manager: The task manager to use.
            middlewares: Optional list of middleware to apply.
        """
        self._server = server
        self._task_manager = task_manager
        self._middlewares = middlewares or []
    
    @classmethod
    def from_agent(
        cls, 
        agent: AgentAdapter, 
        host: str = "localhost", 
        port: int = 8000,
        middlewares: Optional[List[Middleware]] = None
    ) -> "A2aMinServer":
        """Create a server from an agent.
        
        Args:
            agent: The agent to serve.
            host: The host to bind to.
            port: The port to bind to.
            middlewares: Optional list of middleware to apply.
            
        Returns:
            An A2aMinServer instance configured with the agent.
        """
        url = f"http://{host}:{port}/"
        agent_card = agent.get_agent_card(url)
        task_manager = A2aMinTaskManager(agent)
        
        server = A2AServer(
            agent_card=agent_card,
            task_manager=task_manager,
            host=host,
            port=port
        )
        
        return cls(server, task_manager, middlewares)
    
    def start(self):
        """Start the server."""
        self._server.start()
    
    def add_middleware(self, middleware: Middleware):
        """Add middleware to the server.
        
        Args:
            middleware: The middleware to add.
        """
        self._middlewares.append(middleware)