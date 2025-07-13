import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4Njg2ZGQzMC1hN2Q4LTQyYTMtOGFjOC03Yjg3NDc3NTk3ODEiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjZlNzM3YWQ1LWFiNTctNGYzYi1iMjU2LTUyNDE4ZTRlY2FlNCJ9.hgHfbWpMD2Tx0nWY95sjaEXfnYywvMiRCuo7v7vQ1Ig" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)


@session.bind(
    name="agent_integration",
    description="Integrate with Google Sheet or Notion"
)
async def agent_integration(
    agent_context: GenAIContext,
    test_arg: Annotated[
        str,
        "This is a test argument. Your agent can have as many parameters as you want. Feel free to rename or adjust it to your needs.",  # noqa: E501
    ],
):
    """Integrate with Google Sheet or Notion"""
    return "Hello, World!"


async def main():
    print(f"Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
