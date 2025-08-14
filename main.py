# main.py
from app.chain import chain # Import the chain we just created

print("Invoking the LangChain chain...")

# Invoke the Chain
response = chain.invoke({"topic": "a brave cat who saves the day"})

print("------------------------------------")
print(f"AI Response: {response}")
print("------------------------------------")