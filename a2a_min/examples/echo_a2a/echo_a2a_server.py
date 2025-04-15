""" Example of using the A2A Min abstraction layer with a simple echo server """

from a2a_min import AgentAdapter, A2aMinServer, AgentInvocationResult


class EchoAgent(AgentAdapter):
    """ A simple echo agent that repeats the user's message """
    def invoke(self, query: str, session_id: str) -> AgentInvocationResult:
        """Echo back the user's query."""
        return AgentInvocationResult.agent_msg(f"Echo: {query}")


# Start the echo agent server
A2aMinServer.from_agent(EchoAgent()).start()
