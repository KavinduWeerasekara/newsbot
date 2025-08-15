# app/agent.py

from dotenv import load_dotenv
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode # <-- 1. Import ToolNode instead of ToolExecutor
from langchain_tavily import TavilySearch


# Load environment variables
load_dotenv()

# 1. Define the Tools
# We are replacing our fake tool with a real one from Tavily.
# LangChain automatically creates a description for the AI from the tool itself.
search_tool = TavilySearch(max_results = 2)

# The tool_executor is a new component that will execute our tools for us
tool_node = ToolNode([search_tool])

# 2. Define the State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# 3. Define the Nodes
def call_model(state: AgentState):
    """Calls the LLM to decide the next action or respond."""
    print("\n--- NODE: Calling LLM---")
    messages = state['messages']
    model = ChatOpenAI(model = "gpt-4o")

    # We bind the tools to the model every time we call it.
    model_with_tools = model.bind_tools([search_tool])

    response = model_with_tools.invoke(messages)

    return {"messages": [response]}

# def call_tool(state: AgentState):
#     """Calls the appropriate tool with the query from the last AI message."""
#     print("\n--- NODE: Calling Tool ---")
#     last_message = state ['messages'][-1]

#     # The ToolExecutor will take the tool calls from the AI's message
#     # and execute them, returning the results.
#     action = last_message_tool_calls[0]
#     response = tool_executor.invoke(action)

#     # We return the response as a ToolMessage to satisfy the API
#     return {"messages": [response]}

# 4. Define the Edges
def should_continue(state: AgentState):
    """Decides the next step: call a tool or end the conversation."""
    print("\n--- EDGE: Checking for tool calls ---")
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool"
    else:
        return END

# 5. Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tool", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {"tool": "tool", END: END}
)

workflow.add_edge("tool", "agent")
agent_app = workflow.compile()