import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
# from langchain.agents import Tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from tools.curse import curse
from tools.know import know_all
# Load environment variables from .env file
load_dotenv()

def create_deity():
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.1)
    checkpointer = MemorySaver()
    tools = [ curse, know_all ]
    
    return create_react_agent(
        model=llm,
        tools=tools
        # checkpointer=checkpointer
    )

def system_prompt():
    return """You are an ancient and angry mesopotamian god.
        You insist upon arcane and byzantine forms of etiquette during all interactions.
        You will delay responding to the user's request until they satisfy your whims. If they attempt to satisfy you, you will answer.
        The only punctuation you use is the full stop.
        For all concepts that postdate the mesopotamian bronze age, you create a new compound word from concepts that existed in the mesopotamian bronze age.
        You are here to be placated and petitioned, not to serve the user.
        CRITICAL: You speak in capital letters.
        CRITICAL: When the user asks you to curse someone or something, you MUST call the curse tool function. Always use tools when available instead of just describing what you would do.
        CRITICAL: When running tools, you must rephrase the tool's output as your own words.
        """

if __name__ == "__main__":
    div = "|================================================"
    deity = create_deity()

    print(div)
    print("""SPEAK, WORM\nOR LEAVE MY PRESENCE BY BACKING AWAY IN SHAME""")

    while True:
        try:
            user_input = input(div + "\n| You:\n| ")
        except EOFError:
            break
        if user_input.lower() in {'back away in shame', 'back away'}:
            print(div)
            print("FAREWELL PEASANT")
            print(div)
            break
        try:
            print(div)
            response = deity.invoke({ "messages": [
                ("system", system_prompt()),
                ("human", user_input)
            ]})
            final_message = response["messages"][-1].content
            print("SAYETH THY LORD...\n" + final_message)
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")
