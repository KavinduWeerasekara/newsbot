# app/agent.py
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Sequence
import operator
# This is the corrected import line
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_tavily import TavilySearch

# Load environment variables FIRST
load_dotenv()

# Define the Tools
@tool
def search(query: str) -> str:
    """Use this tool to find the most up-to-date information on a person, topic, or event from the internet."""
    print("\n--- NODE: Calling Tavily Search ---")
    tavily_tool = TavilySearch(max_results=2)
    return tavily_tool.invoke(query)

tools = [search]
tool_node = ToolNode(tools)

# Define the State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# Define the Nodes
def call_model(state: AgentState):
    """Calls the LLM to decide the next action or respond."""
    print("\n--- NODE: Calling LLM ---")
    
    # Create the system message to force tool use
    system_message = SystemMessage(
        content="You are a research assistant. You must use the 'search' tool for all user questions to find the most up-to-date information. DO NOT answer from your own knowledge."
    )
    
    # Prepend the system message to the conversation history
    messages = [system_message] + state['messages']

    model = ChatOpenAI(model="gpt-4o")
    model_with_tools = model.bind_tools(tools)
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

# Define the Edges
def should_continue(state: AgentState):
    """Decides the next step: call a tool or end the conversation."""
    print("\n--- EDGE: Checking for tool calls ---")
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "tool"
    else:
        return END

# Build the Graph
workflow = StateGraph(AgentState, config={"recursion_limit": 5})
workflow.add_node("agent", call_model)
workflow.add_node("tool", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tool": "tool",
        END: END,
    }
)
workflow.add_edge("tool", "agent")
agent_app = workflow.compile()