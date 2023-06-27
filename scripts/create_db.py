import sqlite3
from alpaca.trading.client import TradingClient
import sys
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
connection = sqlite3.connect(os.getenv('LOCAL_DB'))
cursor = connection.cursor()


API_URL = os.getenv('ALPACA_API_URL')
API_KEY = os.getenv('APCA_API_KEY_ID')
API_SECRET = os.getenv('ALPACA_API_SECRET')

client = TradingClient(API_KEY, API_SECRET)
assets = client.get_all_assets()

# Create database
cursor.execute("""CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    market TEXT NOT NULL,
    exchange TEXT NOT NULL
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS stock_price (
    id INTEGER PRIMARY KEY,
    stock_id INTEGER,
    date NOT NULL,
    open NOT NULL,
    high NOT NULL,
    low NOT NULL,
    close NOT NULL,
    volume NOT NULL,
    vwap NOT NULL,
    FOREIGN KEY (stock_id) REFERENCES stock(id)
)"""
               )
connection.commit()

cursor.execute("""SELECT symbol,name from stock""")

rows = cursor.fetchall()
symbols = [row[0] for row in rows]
print(f'There are {len(symbols)} stocks available')


for asset in assets:
    if asset.status.name.upper() == 'ACTIVE' and asset.tradable and asset.symbol not in symbols:
        try:
            cursor.execute(
                "INSERT INTO stock (symbol, name, market, exchange) VALUES (? ,?, ?, ?)", (asset.symbol, asset.name, asset.asset_class.name, asset.exchange.name))
        except Exception as e:
            print(e)
            print(asset.name, asset.symbol)

connection.commit()
