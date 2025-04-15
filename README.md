# A2A Minimalistic Python SDK

A minimalistic Python SDK for [Agent-to-Agent (A2A)](https://google.github.io/A2A/#/) communication.

## Overview

The A2A Min SDK provides a Python implementation of the Agent-to-Agent (A2A) protocol, enabling communication between AI agents. The package includes:

- A low-level API for direct interaction with the A2A protocol
- A high-level abstraction layer for simplified usage
- Support for streaming responses
- Support for multimodal content (text, images, structured data)
- Middleware for cross-cutting concerns like logging and metrics

## Installation

You can install the package from PyPI using pip:

```bash
# Using pip
pip install a2a-min

# Using uv
uv pip install a2a-min
```

### Installing From GitHub (develpment version)

To install the latest version directly from GitHub:

```bash
# Using pip
pip install git+https://github.com/pcingola/a2a_min.git

# Using uv
uv pip install git+https://github.com/pcingola/a2a_min.git
```

## Basic Usage

### Creating a Simple Echo Agent Server

Here's how to create a simple server that hosts an echo agent:

```python
from a2a_min import AgentAdapter, A2aMinServer, AgentInvocationResult

class EchoAgent(AgentAdapter):
    """ A simple echo agent that repeats the user's message """
    def invoke(self, query: str, session_id: str) -> AgentInvocationResult:
        """Echo back the user's query."""
        return AgentInvocationResult.agent_msg(f"Echo: {query}")

# Start the echo agent server
A2aMinServer.from_agent(EchoAgent()).start()
```

Save this as `echo_a2a_server.py` and run it to start the server:

```bash
python a2a_min/examples/echo_a2a/echo_a2a_server.py
```

### Creating a Client to Interact with the Agent

Here's how to create a client that connects to the echo agent:

```python
import asyncio
from a2a_min import A2aMinClient

async def client():
    """ Run the example client """
    client = A2aMinClient.connect("http://localhost:8000")
    task = await client.send_message("Hello, Echo Agent!")    
    # Print the response
    for artifact in task.artifacts:
        for part in artifact.parts:
            if hasattr(part, "text"):
                print(f"Response: {part.text}")

if __name__ == "__main__":
    # Run the client
    asyncio.run(client())
```

Save this as `echo_a2a_client.py` and run it to interact with the server:

```bash
 python a2a_min/examples/echo_a2a/echo_a2a_client.py
```

## Creating Custom Agents

To create your own agent, extend the `AgentAdapter` class and implement the `invoke` method:

```python
from a2a_min import AgentAdapter, AgentInvocationResult

class MyCustomAgent(AgentAdapter):
    def invoke(self, query: str, session_id: str) -> AgentInvocationResult:
        # Process the query and generate a response
        response = f"You asked: {query}. Here's my response..."
        return AgentInvocationResult.agent_msg(response)
```

## Advanced Features

### Streaming Responses

To create an agent that streams its response:

```python
import asyncio
from a2a_min import AgentAdapter, AgentInvocationResult

class StreamingAgent(AgentAdapter):
    async def stream(self, query: str, session_id: str):
        words = f"You asked: {query}. This is a streaming response.".split()
        
        for i, word in enumerate(words):
            partial_text = " ".join(words[:i+1])
            
            yield AgentInvocationResult.agent_msg(
                partial_text,
                is_complete=(i == len(words) - 1)
            )
            
            await asyncio.sleep(0.2)
```

To receive streaming responses in the client:

```python
async def streaming_client():
    client = A2aMinClient.connect("http://localhost:8000")
    async for update in client.send_message_streaming("Hello, Streaming Agent!"):
        if update.artifact:
            for part in update.artifact.parts:
                if hasattr(part, "text"):
                    print(f"Partial response: {part.text}")
```

### Multimodal Support

To create an agent that can respond with text, images, and structured data:

```python
from a2a_min import AgentAdapter, AgentInvocationResult
from a2a_min.types import Message, TextPart, FilePart, FileContent, DataPart

class MultiModalAgent(AgentAdapter):
    def invoke(self, query: str, session_id: str) -> AgentInvocationResult:
        # Create a multimodal response with text, image, and data
        message = Message(
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
        )
        
        return AgentInvocationResult(
            message=message,
            is_complete=True,
            requires_input=False
        )
```

### Using Middleware

You can add middleware to your server for logging, metrics, or other cross-cutting concerns:

```python
from a2a_min import A2aMinServer, LoggingMiddleware, MetricsMiddleware

# Create middleware
logging_middleware = LoggingMiddleware()

def record_metric(name, value):
    print(f"Metric {name}: {value}")

metrics_middleware = MetricsMiddleware(record_metric)

# Create server with middleware
server = A2aMinServer.from_agent(
    MyCustomAgent(),
    middlewares=[logging_middleware, metrics_middleware]
)
server.start()
```

## Examples

The package includes several examples to demonstrate its usage:

- `a2a_min/examples/echo_a2a`: A simple echo agent example
- `a2a_min/examples/streaming_agent_example.py`: An agent that streams its response
- `a2a_min/examples/multimodal_agent_example.py`: An agent that responds with text, images, and data
- `a2a_min/examples/base`: Low-level API examples

To run the echo example:

1. Start the server in one terminal:
   ```bash
   python -m a2a_min.examples.echo_a2a.echo_a2a_server
   ```

2. Run the client in another terminal:
   ```bash
   python -m a2a_min.examples.echo_a2a.echo_a2a_client
   ```

## Documentation

For more detailed documentation, see:

- `a2a_min/docs/abstraction_readme.md`: Overview of the abstraction layer
- `a2a_min/docs/new_abstraction.md`: Detailed design of the abstraction layer

## Benefits of Using a2a_min

- **Simplified API**: The abstraction layer provides a much simpler API for both client and server sides
- **Type Safety**: All components use Pydantic models for strong typing
- **Extensibility**: Clear extension points for middleware, logging, etc.
- **Optional Features**: Streaming and push notifications are optional but easy to enable
- **Consistent Naming**: Method names are aligned with current type names
- **Reuse Existing Types**: Leverages the current type system for compatibility
