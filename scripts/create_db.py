import sqlite3
import alpaca_trade_api as tradeapi
import sys
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
connection = sqlite3.connect('app.db')
cursor = connection.cursor()


API_URL = os.getenv('ALPACA_API_URL')
API_KEY = os.getenv('APCA_API_KEY_ID')
API_SECRET = os.getenv('ALPACA_API_SECRET')

api = tradeapi.REST(API_KEY, API_SECRET, API_URL)
assets = api.list_assets()

# Create database
cursor.execute("""CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL UNIQUE,
    company TEXT NOT NULL
)"""
               )

cursor.execute("""CREATE TABLE IF NOT EXISTS stock_price (
    id INTEGER PRIMARY KEY,
    stock_id INTEGER,
    date NOT NULL,
    open NOT NULL,
    high NOT NULL,
    low NOT NULL,
    close NOT NULL,
    adjusted_close NOT NULL,
    volume NOT NULL,
    FOREIGN KEY (stock_id) REFERENCES stock(id)
)"""
               )
connection.commit()

cursor.execute("""SELECT symbol,company from stock""")

rows = cursor.fetchall()
symbols = [row[0] for row in rows]


for asset in assets:
    if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
        try:
            cursor.execute(
                "INSERT INTO stock (symbol, company) VALUES (? ,?)", (asset.symbol, asset.name))
        except Exception as e:
            print(e)
            print(asset.name, asset.symbol)

connection.commit()
