# A2A Minimalistic Python SDK

A minimalistic Python SDK for [Agent-to-Agent (A2A)](https://google.github.io/A2A/#/) communication.

## Installation

### Requirements
- Python >= 3.12.2


### From GitHub

To install the latest version directly from GitHub:

```bash
# Using pip
pip install git+https://github.com/pcingola/a2a_min.git

# Using uv
uv pip install git+https://github.com/pcingola/a2a_min.git
```

### Development Installation

For development purposes, clone the repository and install in editable mode:

```bash
# Clone the repository
git clone https://github.com/pcingola/a2a_min.git
cd a2a_min

# Install in editable mode
pip install -e .
# or with uv
uv pip install -e .
```

## Features

- Client for communicating with A2A-compatible agents
- Server for implementing A2A-compatible agents
- Support for streaming responses
- Push notification support
- Task management

## Basic Usage

### Client

```python
import asyncio
from a2a_min import A2AClient, TextPart, Message

async def main():
    # Create a client
    client = A2AClient(url="https://example.com/agent")
    
    # Create a message
    message = Message(
        role="user",
        parts=[TextPart(text="Hello, agent!")]
    )
    
    # Send a task
    response = await client.send_task({
        "id": "task-123",
        "message": message.model_dump()
    })
    
    print(f"Task ID: {response.result.id}")
    print(f"Task Status: {response.result.status.state}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Server

```python
from a2a_min import A2AServer, TaskManager, AgentCard, AgentProvider, AgentCapabilities, AgentSkill

# Create an agent card
agent_card = AgentCard(
    name="Example Agent",
    description="An example A2A agent",
    url="http://localhost:5000",
    provider=AgentProvider(
        organization="Example Org",
        url="https://example.org"
    ),
    version="1.0.0",
    capabilities=AgentCapabilities(
        streaming=True,
        pushNotifications=True,
        stateTransitionHistory=True
    ),
    skills=[
        AgentSkill(
            id="example",
            name="Example Skill",
            description="An example skill"
        )
    ]
)

# Create a task manager
task_manager = TaskManager()

# Create and start the server
server = A2AServer(
    host="0.0.0.0",
    port=5000,
    agent_card=agent_card,
    task_manager=task_manager
)

server.start()
```

## License

MIT