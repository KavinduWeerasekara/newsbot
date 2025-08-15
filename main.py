# main.py
from app.agent import agent_app
from langchain_core.messages import HumanMessage

def run_agent():
    # Define the initial input for the agent
    inputs = {"messages": [HumanMessage(content="What is the weather in Colombo?")]}
    
    # Stream the agent's responses
    for event in agent_app.stream(inputs):
        for value in event.values():
            print(value['messages'][-1].content)
            print("---")

if __name__ == "__main__":
    run_agent()