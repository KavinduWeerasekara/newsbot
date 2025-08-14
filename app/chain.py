# app/chain.py
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables FROM THIS FILE
load_dotenv()

# Create a Prompt Template
prompt = ChatPromptTemplate.from_template(
    "Write a single, short sentence about {topic}."
)

# Initialize the Model
model = ChatOpenAI(model="gpt-3.5-turbo")

# Create an Output Parser
output_parser = StrOutputParser()

# Create the Chain
chain = prompt | model | output_parser