from a2a_min.examples.base.agent_task_manager import AgentTaskManager
from a2a_min.examples.base.dummy_agent import DummyAgent
from a2a_min.base.server import A2AServer
from a2a_min.base.types import AgentCard, AgentCapabilities, AgentSkill
from a2a_min.base.utils.push_notification_auth import PushNotificationSenderAuth

import click
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--host", "host", default="localhost")
@click.option("--port", "port", default=10000)
def main(host, port):
    """Starts the Currency Agent server."""
    try:
        skill = AgentSkill(
            id="dummy_agent",
            name="Dummy Agent",
            description="Pretneds to be a usefull agent...",
            tags=["dummy", "fake"],
            examples=["Are you a real agent?", "What is the meaning of life?"],
        )
        
        capabilities = AgentCapabilities(streaming=True, pushNotifications=True)

        agent_card = AgentCard(
            name=skill.name,
            description=skill.description,
            url=f"http://{host}:{port}/",
            version="1.0.0",
            capabilities=capabilities,
            skills=[skill],
        )

        notification_sender_auth = PushNotificationSenderAuth()
        notification_sender_auth.generate_jwk()
        
        server = A2AServer(
            agent_card=agent_card,
            task_manager=AgentTaskManager(agent=DummyAgent(), notification_sender_auth=notification_sender_auth),
            host=host,
            port=port,
        )

        server.app.add_route(
            "/.well-known/jwks.json", notification_sender_auth.handle_jwks_endpoint, methods=["GET"]
        )

        logger.info(f"Starting server on {host}:{port}")
        server.start()
    except Exception as e:
        import traceback
        logger.error(f"An error occurred during server startup: {e}")
        logger.error(traceback.format_exc())
        exit(1)


if __name__ == "__main__":
    main()
