import uuid

from agents import CascadingAgent, ReceiveMessageEvent
from autogen_core.application import WorkerAgentRuntime
from autogen_core.base import try_get_known_serializers_for_type


async def main() -> None:
    runtime = WorkerAgentRuntime(host_address="localhost:50051")
    runtime.add_message_serializer(try_get_known_serializers_for_type(ReceiveMessageEvent))
    runtime.start()
    agent_type = f"cascading_agent_{uuid.uuid4()}".replace("-", "_")
    await CascadingAgent.register(runtime, agent_type, lambda: CascadingAgent(max_rounds=3))
    await runtime.stop_when_signal()


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("autogen_core")
    import asyncio

    asyncio.run(main())
