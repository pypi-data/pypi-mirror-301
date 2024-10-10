import os
from os import environ
from typing import Any

from autogen.agentchat import ConversableAgent
from fastapi import FastAPI

from fastagency import UI
from fastagency.adapters.nats import NatsAdapter
from fastagency.logging import get_logger
from fastagency.runtimes.autogen.autogen import AutoGenWorkflows

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.0,
}

logger = get_logger(__name__)

wf = AutoGenWorkflows()


@wf.register(name="simple_learning", description="Student and teacher learning chat")
def simple_workflow(ui: UI, workflow_uuid: str, params: dict[str, Any]) -> str:
    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="I can help you learn about geometry. What subject you would like to explore?",
        workflow_uuid=workflow_uuid,
    )

    student_agent = ConversableAgent(
        name="Student_Agent",
        system_message="You are a student willing to learn.",
        llm_config=llm_config,
        # human_input_mode="ALWAYS",
    )
    teacher_agent = ConversableAgent(
        name="Teacher_Agent",
        system_message="You are a math teacher.",
        llm_config=llm_config,
        # human_input_mode="ALWAYS",
    )

    logger.info("Above initiate_chat in simple_workflow")
    logger.info(llm_config)
    chat_result = student_agent.initiate_chat(
        teacher_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=5,
    )
    logger.info("Below initiate_chat in simple_workflow")
    logger.info(chat_result)

    return chat_result.summary


nats_url = environ.get("NATS_URL", None)  # type: ignore[assignment]

user: str = "faststream"
password: str = environ.get("FASTSTREAM_NATS_PASSWORD")  # type: ignore[assignment]

adapter = NatsAdapter(provider=wf, nats_url=nats_url, user=user, password=password)

app = FastAPI(lifespan=adapter.lifespan)


# this is optional, but we would like to see the list of workflows
@app.get("/")
def list_workflows():
    return {"Workflows": {name: wf.get_description(name) for name in wf.names}}


# start the provider with either command
# uvicorn 1_main_natsprovider:app --reload
