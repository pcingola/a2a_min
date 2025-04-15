"""Example of using the A2A Min abstraction layer with a streaming agent."""

import asyncio
from a2a_min import AgentAdapter, AgentInvocationResult


class StreamingAgent(AgentAdapter):
    """A simple agent that streams its response word by word."""
    
    @property
    def capabilities(self):
        capabilities = super().capabilities
        capabilities.streaming = True
        return capabilities
    
    def invoke(self, query: str, session_id: str) -> AgentInvocationResult:
        """Generate a response to the query."""
        return AgentInvocationResult.agent_msg(f"You asked: {query}. This is a non-streaming response.")
    
    async def stream(self, query: str, session_id: str):
        """Stream a response word by word.\n"""
        # Generate a response
        words = f"You asked: {query}. This is a streaming response that comes word by word.".split()
        # Stream partial responses
        for i, word in enumerate(words):
            yield AgentInvocationResult.agent_msg(f"{word} ", is_complete=False)
            await asyncio.sleep(0.2)  # Simulate some processing time        
        yield AgentInvocationResult.agent_msg(f"\n{' '.join(words)}") # Yield the final answer
