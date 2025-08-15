# app/agent.py
import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# 1. Define the State
# This is the "memory" of our agent. It's a dictionary that holds the
# conversation messages.
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# 2. Define the Tools
# For now, we'll create a simple, fake search tool.
def search_tool(query: str):
    """Use this tool to find the current weather for a specific city."""
    print(f"\n--- TOOL: Searching for '{query}' ---")
    # In a real app, this would perform a web search.
    return f"The weather in {query} is 30 degrees Celsius and sunny."

# 3. Define the Nodes
# Nodes are the steps in our graph. Each node is a function.

# A more explicit and robust version of the call_model node

def call_model(state: AgentState):
    """Calls the LLM to decide the next action or respond."""
    print("\n--- NODE: Calling LLM ---")
    messages = state['messages']
    model = ChatOpenAI(model="gpt-4o")
    
    # 1. Define the list of tools we want the model to know about.
    tools = [search_tool]
    
    # 2. Bind the tools to the model. This creates a new model
    #    instance that is aware of our tools.
    model_with_tools = model.bind_tools(tools)
    
    # 3. Invoke the model that now has the tool "manual".
    response = model_with_tools.invoke(messages)
    
    return {"messages": [response]}

def call_tool(state: AgentState):
    """Calls the search tool with the query from the last AI message."""
    print("\n--- NODE: Calling Tool ---")
    last_message = state['messages'][-1] # Get the last message
    
    # Extract the tool call information from the AI's message
    tool_call = last_message.tool_calls[0]
    tool_name = tool_call['name']
    tool_args = tool_call['args']

    if tool_name == "search_tool":
        result = search_tool(tool_args['query'])
        return {"messages": [ToolMessage(content=result, tool_call_id=tool_call['id'])]}
    else:
        return {"messages": [Message(content="Tool not found.")]}

# 4. Define the Edges
# Edges decide which node to go to next.

def should_continue(state: AgentState):
    """Decides the next step: call a tool or end the conversation."""
    print("\n--- EDGE: Checking for tool calls ---")
    last_message = state['messages'][-1]
    
    # If the last message has tool calls, we route to the 'call_tool' node
    if last_message.tool_calls:
        return "tool"
    # Otherwise, we end the conversation
    else:
        return END

# 5. Build the Graph
# This is where we wire up all the nodes and edges.
workflow = StateGraph(AgentState)

# Add the nodes
workflow.add_node("agent", call_model)
workflow.add_node("tool", call_tool)

# Define the edges
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

# Compile the graph into a runnable app
agent_app = workflow.compile()