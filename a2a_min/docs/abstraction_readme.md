# A2A Min Abstraction Layer

This document provides an overview of the A2A Min abstraction layer, which simplifies the usage of the A2A Min client-server architecture.

## Overview

The abstraction layer provides a simplified API for both client and server sides, making it easier to create and use A2A agents. It builds on top of the existing A2A Min implementation, providing a more user-friendly interface while maintaining all the functionality.

## Key Components

### BaseAgent

The `BaseAgent` class is the base class for all agents. It defines the interface that all agents must implement.

```python
from a2a_min import BaseAgent, AgentInvocationResult
from a2a_min.types import Message, TextPart

class MyAgent(BaseAgent):
    def invoke(self, query: str, session_id: str) -> AgentInvocationResult:
        return AgentInvocationResult(
            message=Message(
                role="agent",
                parts=[TextPart(text=f"You said: {query}")]
            ),
            is_complete=True,
            requires_input=False
        )
```

### A2aMinClient

The `A2aMinClient` class provides a simplified client for interacting with A2A servers.

```python
from a2a_min import A2aMinClient

# Connect to a server
client = A2aMinClient.connect("http://localhost:8000")

# Send a message
task = await client.send_message("Hello, agent!")

# Access the response
for artifact in task.artifacts:
    for part in artifact.parts:
        if hasattr(part, "text"):
            print(part.text)
```

### A2aMinServer

The `A2aMinServer` class provides a simplified server for hosting A2A agents.

```python
from a2a_min import A2aMinServer, BaseAgent

# Create an agent
agent = MyAgent()

# Create and start a server
server = A2aMinServer.from_agent(agent)
server.start()
```

### Middleware

The abstraction layer includes middleware support for adding cross-cutting concerns like logging, metrics, and debugging.

```python
from a2a_min import A2aMinServer, LoggingMiddleware, MetricsMiddleware

# Create middleware
logging_middleware = LoggingMiddleware()

def record_metric(name, value):
    print(f"Metric {name}: {value}")

metrics_middleware = MetricsMiddleware(record_metric)

# Create server with middleware
server = A2aMinServer.from_agent(
    agent,
    middlewares=[logging_middleware, metrics_middleware]
)
```

## Features

### Streaming Support

The abstraction layer supports streaming responses, allowing agents to send partial responses as they're generated.

```python
from a2a_min import BaseAgent, AgentInvocationResult
from a2a_min.types import Message, TextPart

class StreamingAgent(BaseAgent):
    async def stream(self, query: str, session_id: str):
        words = f"You asked: {query}. This is a streaming response.".split()
        
        for i, word in enumerate(words):
            partial_text = " ".join(words[:i+1])
            
            yield AgentInvocationResult(
                message=Message(
                    role="agent",
                    parts=[TextPart(text=partial_text)]
                ),
                is_complete=(i == len(words) - 1),
                requires_input=False
            )
            
            await asyncio.sleep(0.2)
```

### Multimodal Support

The abstraction layer supports multimodal responses, allowing agents to send text, images, and structured data.

```python
from a2a_min import BaseAgent, AgentInvocationResult
from a2a_min.types import Message, TextPart, FilePart, FileContent, DataPart

class MultiModalAgent(BaseAgent):
    def invoke(self, query: str, session_id: str) -> AgentInvocationResult:
        return AgentInvocationResult(
            message=Message(
                role="agent",
                parts=[
                    TextPart(text="Here's an image and some data:"),
                    FilePart(
                        file=FileContent(
                            name="example.jpg",
                            mimeType="image/jpeg",
                            uri="https://example.com/image.jpg"
                        )
                    ),
                    DataPart(
                        data={
                            "temperature": 72.5,
                            "unit": "Fahrenheit",
                            "conditions": "Sunny"
                        }
                    )
                ]
            ),
            is_complete=True,
            requires_input=False
        )
```

## Examples

The abstraction layer includes several examples to demonstrate its usage:

- `echo_agent_example.py`: A simple echo agent that repeats the user's message.
- `streaming_agent_example.py`: An agent that streams its response word by word.
- `multimodal_agent_example.py`: An agent that can respond with text, images, and structured data.

To run the examples:

1. Start the server in one terminal:
   ```
   python -m a2a_min.examples.echo_agent_example server
   ```

2. Run the client in another terminal:
   ```
   python -m a2a_min.examples.echo_agent_example client
   ```

## Benefits

- **Simplified API**: The abstraction layer provides a much simpler API for both client and server sides.
- **Type Safety**: All components use Pydantic models for strong typing.
- **Extensibility**: Clear extension points for middleware, logging, etc.
- **Optional Features**: Streaming and push notifications are optional but easy to enable.
- **Consistent Naming**: Method names are aligned with current type names.
- **Reuse Existing Types**: Leverages the current type system for compatibility.