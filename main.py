# main.py
import logging
from app.chain import chain
from app.database import get_fact, init_db, add_fact

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Main Application Logic ---

def run_agent(topic: str):

    # 1. Initialize the database
    init_db()

    # 2. Check the database (memory) first
    logging.info(f"Searching for information on '{topic}'...")

    known_fact = get_fact(topic)

    if known_fact:

        # 3a. If fact is in memory, use it

        print("------------------------------------")
        print("[RESPONSE FROM DATABASE MEMORY]")
        print(f"Fact: {known_fact}")
        print("------------------------------------")

    else:

        # 3b. If not in memory, call the AI

        print("[CALLING LLM - THIS MAY TAKE A MOMENT]")
        new_fact = chain.invoke({"topic": topic})

        print("------------------------------------")
        print("[RESPONSE FROM LLM]")
        print(f"Fact: {new_fact}")
        print("------------------------------------")

        # 4. Save the new fact to memory for next time
        add_fact(topic, new_fact)

if __name__ == "__main__":

    # We will ask about the same topic to test the memory

    topic_to_research = "the history of the Eifel Tower"
    run_agent(topic_to_research)