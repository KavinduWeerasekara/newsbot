# main.py
from app.agent import agent_app
from langchain_core.messages import HumanMessage, AIMessage

def run_agent(question: str):
    print(f"\n--- Running Agent for: '{question}' ---")
    inputs = {"messages": [HumanMessage(content=question)]}
    
    print("Agent is thinking...")
    for event in agent_app.stream(inputs):
        for value in event.values():
            last_message = value['messages'][-1]
            if isinstance(last_message, AIMessage) and not last_message.tool_calls:
                print("\n--- FINAL RESPONSE ---")
                print(last_message.content)

if __name__ == "__main__":
    # 1. Ask a question that should use the RAG tool
    run_agent("What was the client feedback about Sparky's color in the Cosmic Quest project?")
    
    # 2. Ask a question that should use the web search tool
    run_agent("What is the latest news about the James Webb Space Telescope?")