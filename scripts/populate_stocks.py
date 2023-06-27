import sqlite3
import alpaca_trade_api as tradeapi
import sys
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
connection = sqlite3.connect(os.getenv('LOCAL_DB'))
cursor = connection.cursor()


API_URL = os.getenv('ALPACA_API_URL')
API_KEY = os.getenv('APCA_API_KEY_ID')
API_SECRET = os.getenv('ALPACA_API_SECRET')
api = tradeapi.REST(API_KEY, API_SECRET, API_URL)

cursor.execute("""SELECT symbol ,name, id from stock""")

rows = cursor.fetchall()
symbols = [row[0] for row in rows]

stock_dict = {}
print(f'There are {len(symbols)} stocks available')
chunk_size = 200
# # barsets = api.get_barset()
for row in rows:
    symbol = row[0]
    stock_dict[symbol] = row[2]

for i in range(0, len(symbols), chunk_size):
    symbol_chunck = symbols[i: i+chunk_size]
    barset = api.get_barset(symbol_chunck, 'day')

    for symbol in barset:
        print(f"Processing symbol: {symbol}")
        for bar in barset[symbol]:
            stock_id = stock_dict[symbol]
            cursor.execute(""""
                INSERT INTO stock_price (stock_id, date, open, high, low, close, volume)
                VALUES ((SELECT if from stock WHERE ), ?,?,?,?,?,?)
            """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))

connection.commit()
