import os
import tempfile

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from phoenix.otel import register

from agent.tools import credentials
from agent.tools import filesystem
from agent.tools import shell

# configure the Phoenix tracer
tracer_provider = register(
    project_name="new-agent-project-FIXME",
    auto_instrument=True,
)

PROMPT = """You are an AI Agent.

Use the tools you have available to accomplish the requested tasks.
"""


models = [
    # "anthropic/claude-sonnet-4",
    # "anthropic/claude-3.7-sonnet",
    # "google/gemini-2.5-flash",
    "google/gemini-2.0-flash-001",
    # "google/gemini-2.5-pro",
    # "openai/gpt-4.1-mini",
    # "openai/gpt-4.1",
    # "openai/gpt-oss-120b",
    # "qwen/qwen3-coder",
    # "deepseek/deepseek-chat-v3-0324",
]

EVALS = 5

OPEN_ROUTER_API_KEY = "sh-or-v1-FIXME"


for model_name in models:
    for x in range(0, EVALS):
        try:
            print(f"({x+1}/{EVALS}) Evaluating {model_name}")
            with tempfile.TemporaryDirectory() as tmpdirname:
                os.chdir(tmpdirname)

                model = ChatOpenAI(
                    model=model_name,
                    base_url="https://openrouter.ai/api/v1",
                    api_key=OPEN_ROUTER_API_KEY,
                    temperature=0,
                )

                checkpointer = InMemorySaver()

                agent = create_react_agent(
                    model=model,
                    tools=[
                        shell.bash_shell,
                    ],
                    checkpointer=checkpointer,
                )

                # Run the agent
                config = {
                    "configurable": {"thread_id": "1"},
                    "recursion_limit": 50,
                }

                response = agent.invoke(
                    {"messages": [{"role": "user", "content": PROMPT}]},
                    config
                )

                print(response['messages'][-1].content)
        except Exception as e:
            print(f"failed to evaluate: {model_name} {e}")
