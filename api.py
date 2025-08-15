# api.py
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import agent_app
# Import both HumanMessage and AIMessage
from langchain_core.messages import HumanMessage, AIMessage

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- API Setup ---
app = FastAPI(
    title="NewsBot Agent API",
    description="An API for interacting with a research agent.",
    version="1.0.0",
)

# Define the request model
class AgentRequest(BaseModel):
    question: str

# --- API Endpoints ---
@app.post("/invoke")
async def invoke_agent(request: AgentRequest):
    """
    Receives a question, runs the agent, and returns the final response.
    """
    logging.info(f"Received request: {request.question}")

    inputs = {"messages": [HumanMessage(content=request.question)]}
    
    final_response = ""
    # Use .stream() to get the final answer
    for event in agent_app.stream(inputs):
        for value in event.values():
            last_message = value['messages'][-1]
            
            # --- THIS IS THE CORRECTED LOGIC ---
            # First, check if the message is an AIMessage
            if isinstance(last_message, AIMessage):
                # If it's an AIMessage, check if it's a tool call or a final answer
                if not last_message.tool_calls:
                    # It's a final answer, so we store it
                    final_response = last_message.content

    logging.info(f"Generated final response: {final_response}")
    return {"response": final_response}