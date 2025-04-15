"""Example of using the A2A Min abstraction layer with a streaming server."""

from a2a_min import A2aMinServer
from a2a_min.examples.streaming_a2a.streaming_a2a_agent import StreamingAgent


if __name__ == "__main__":
    server = A2aMinServer.from_agent(StreamingAgent())
    server.start()
