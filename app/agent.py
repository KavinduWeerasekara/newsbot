# app/agent.py
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from app.rag import run_rag_query # <-- Import our new RAG function

# Load environment variables
load_dotenv()

# --- 1. DEFINE TOOLS ---
@tool
def web_search(query: str) -> str:
    """Use this tool to find the most up-to-date information on a person, topic, or event from the internet."""
    from langchain_tavily import TavilySearch
    tavily_tool = TavilySearch(max_results=2)
    return tavily_tool.invoke(query)

@tool
def project_knowledge_base(query: str) -> str:
    """
    Use this tool to find specific information about the 'Cosmic Quest' project,
    including creative direction, client feedback, and technical details.
    """
    return run_rag_query(query)

# Create a list of all our tools and the ToolNode
tools = [web_search, project_knowledge_base]
tool_node = ToolNode(tools)

# --- 2. DEFINE STATE & NODES ---
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

def call_model(state: AgentState):
    """Calls the LLM to decide the next action or respond."""
    print("\n--- NODE: Calling LLM ---")
    messages = state['messages']
    model = ChatOpenAI(model="gpt-4o")
    model_with_tools = model.bind_tools(tools)
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

# --- 3. DEFINE EDGES ---
def should_continue(state: AgentState):
    """Decides the next step: call a tool or end the conversation."""
    print("\n--- EDGE: Checking for tool calls ---")
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "tool"
    else:
        return END

# --- 4. BUILD GRAPH ---
workflow = StateGraph(AgentState, config={"recursion_limit": 5})
workflow.add_node("agent", call_model)
workflow.add_node("tool", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"tool": "tool", END: END})
workflow.add_edge("tool", "agent")
agent_app = workflow.compile()