from dotenv import load_dotenv
from agents import Agent, Runner, trace
import os
import asyncio


load_dotenv(override=True)

openai_api_key= os.getenv("OPENAI_API_KEY")


agent = Agent(name="jockster", instructions="you are an jock teller", model="gpt-4o-mini")
async def main():
    result= await Runner.run(agent, "tell a jock on AI")
    print(result)
    # print(result.final_output)
    
asyncio.run(main())