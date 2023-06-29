import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
connection = sqlite3.connect(os.getenv("LOCAL_DB"))
cursor = connection.cursor()

# Create database
cursor.execute("""DROP TABLE stock_price""")
cursor.execute("""DROP TABLE stock""")


connection.commit()
