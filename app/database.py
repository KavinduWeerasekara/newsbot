
import sqlite3
import logging

DATABASE_FILE = "memory.db"

def init_db():

    """Initializes the database and creates the facts table if it doesn't exist."""
    try:
        con = sqlite3.connect(DATABASE_FILE)
        cur = con.cursor()

        # Create table with a topic (PRIMARY KEY means it must be unique) and the fact text

        cur.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                topic TEXT PRIMARY KEY,
                fact TEXT NOT NULL
            )
        """)

        con.commit()
        con.close()
        logging.info("Database initialized successfully.")
    
    except Exception as e:
        logging.error(f"Error initializing database: {e}")




def add_fact(topic: str, fact: str):
    """Adds a new fact to the database."""
    try:
        con = sqlite3.connect(DATABASE_FILE)
        cur = con.cursor()
        # The SQL command must be a standard string.
        # The table name 'facts' is part of the string itself.
        cur.execute("INSERT INTO facts (topic, fact) VALUES (?, ?)", (topic, fact))
        con.commit()
        con.close()
        logging.info(f"Added fact for topic: {topic}")
    except sqlite3.IntegrityError:
        logging.warning(f"Topic '{topic}' already exists in the database. Not adding.")
    except Exception as e:
        logging.error(f"Error adding fact: {e}")



def get_fact(topic: str) -> str | None:

    """Retrieves a fact from the database by topic."""
    try:
        con = sqlite3.connect(DATABASE_FILE)
        cur = con.cursor()
        cur.execute("SELECT fact FROM facts WHERE topic = ?", (topic,))
        
        # fetchone() gets the first result
        result = cur.fetchone()
        con.close()
        if result:
            logging.info(f"Found fact for topic '{topic}' in database.")
            return result[0] # The result is a tuple, e.g., ('fact text',), so we take the first item
        else:
            logging.info(f"No fact found for topic '{topic}' in database.")
            return None
    except Exception as e:
        logging.error(f"Error getting fact: {e}")
        return None

