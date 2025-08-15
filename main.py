# main.py
from app.agent import agent_app
from langchain_core.messages import HumanMessage, AIMessage

def run_agent():
    # Ask a question that requires up-to-date information
    inputs = {"messages": [HumanMessage(content="What is the latest news about Trump")]}
    
    
    for event in agent_app.stream(inputs):
        for value in event.values():
            last_message = value['messages'][-1]
            # This is our new, smarter filter:
            # Only print the content if the last message is from the AI
            # and it is NOT a tool call. This is the final answer.
            if isinstance(last_message, AIMessage) and not last_message.tool_calls:
                print("\n--- FINAL RESPONSE ---")
                print(last_message.content)

if __name__ == "__main__":
    run_agent()