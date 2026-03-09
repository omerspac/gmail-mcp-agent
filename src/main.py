import asyncio
import os

from agents import Agent, Runner, set_tracing_disabled
from agents.mcp import MCPServerStdio
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

set_tracing_disabled(disabled = True)

api_key = os.getenv("LLM_API_KEY")

if not api_key:
    raise ValueError("LLM_API_KEY is not set.")

gmail_token = os.getenv("GMAIL_TOKEN")
if not gmail_token:
    raise ValueError("GMAIL_TOKEN is not set in .env file.")

external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)

llm_model = OpenAIChatCompletionsModel(
    model="openrouter/free",
    openai_client=external_client
)


async def main():
    print("🚀 Starting MCP Agent...\n")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(script_dir, "gmail_server.py")
      
    async with MCPServerStdio(
        params={
            "command": "python",
            "args": [server_path],
            "env": {
                "GMAIL_TOKEN": gmail_token
            }
        }
    ) as mcp_server:
        print("✅ Connected to MCP Server!\n")

        agent = Agent(
            name="GMAIL AI Assistant",
            model=llm_model,
            instructions="""
            You are a personal AI-Powered Gmail Assistant.
            You have access to Gmail tools via MCP server.
            Use the available tools whenever needed to complete tasks.
            
            For bulk operations (sending multiple emails):
            - Process them in smaller batches if needed
            - If you encounter an error, report what was completed successfully
            - Keep responses concise to avoid context overflow
            """,
            mcp_servers=[mcp_server],
        )

        print("💬 Chat with your Gmail Assistant! (Type 'quit' or 'exit' to stop)\n")
        
        while True:
            task = input("You: ")
            
            if task.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not task.strip():
                continue
            
            try:
                result = await Runner.run(
                    agent,
                    input=task
                )
                
                print(f"🤖 Gmail Assistant: {result.final_output}\n")
            
            except Exception as e:
                print(f"❌ Error: {str(e)}\n")
                print("Let's try again. You can rephrase your request or try a simpler task.\n")

if __name__ == "__main__":
    asyncio.run(main())