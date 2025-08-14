# main.py

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core_prompts import ChatPromptTemplate
from langchain_core.output_parser import StrOutParser

# Load environment variables from .env file
load_dotenv()

# 1. Create a Prompt Template
# This template will take a "topic" variable and insert it into the prompt.

prompt = ChatPromptTemplate.from_template(
    "write a Single, short sentense about {topic}"
)

# 2. Initialize the Model
# This creates a wrapper around the OpenAI model.

model = ChatOpenAI(model = "gpt-3.5-turbo")

# 3. Create an Output Parser
# This will take the AI's message object and convert it into a simple string.

output_parser = StrOutputParser()

# 4. Create the Chain using LCEL (the | symbol)
# This is the core of LangChain. We are "piping" the components together.
# The output of the prompt flows into the model, and the model's
# output flows into the parser.

chain = prompt | model | output_parser

print("invoking the Langchain chain...")

# 5. Invoke the Chain
# We run the entire chain by calling .invoke() and passing the
# input variables as a dictionary.

response = chain.invoke({"topic": "a brave cat who saves the day"})

print("__________________________________________________")
print(f"AI Response: {response}")
print("__________________________________________________")