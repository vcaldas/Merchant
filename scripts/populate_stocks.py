import os
import sqlite3
from datetime import datetime

from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from dotenv import load_dotenv

load_dotenv()
connection = sqlite3.connect(os.getenv("LOCAL_DB"))
cursor = connection.cursor()


API_URL = os.getenv("ALPACA_API_URL")
API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("ALPACA_API_SECRET")
client = TradingClient(API_KEY, API_SECRET)
assets = client.get_all_assets()

cursor.execute("""SELECT symbol ,name, id from stock""")

rows = cursor.fetchall()
symbols = [row[0] for row in rows]

stock_dict = {}
print(f"There are {len(symbols)} stocks available")
chunk_size = 200
# # barsets = api.get_barset()
for row in rows:
    symbol = row[0]
    stock_dict[symbol] = row[2]


cursor.execute("""SELECT symbol ,name, id, market FROM stock WHERE market = 'CRYPTO'""")
client = CryptoHistoricalDataClient()

rows = cursor.fetchall()

symbols = [row[0] for row in rows]

stock_dict = {}
print(f"There are {len(symbols)} Cryptos available")
chunk_size = 200
# # barsets = api.get_barset()
for row in rows:
    symbol = row[0]
    stock_dict[symbol] = row[2]


for i in range(0, len(symbols), chunk_size):
    symbol_chunck = symbols[i : i + chunk_size]
    # no keys required for crypto data

    request_params = CryptoBarsRequest(
        symbol_or_symbols=symbol_chunck,
        timeframe=TimeFrame.Day,
        start=datetime(2023, 1, 1),
    )
    bars = client.get_crypto_bars(request_params)
    for _symbol in symbol_chunck:
        bar = bars[_symbol]
        stock_id = stock_dict[_symbol]
        for entry in bar:
            cursor.execute(
                """
            INSERT INTO stock_price (stock_id, date, open, high, low, close, volume, vwap)
            VALUES (?, ?,?,?,?,?,?, ?)
        """,
                (
                    stock_id,
                    entry.timestamp.date().isoformat(),
                    entry.open,
                    entry.high,
                    entry.low,
                    entry.close,
                    entry.volume,
                    entry.vwap,
                ),
            )

    connection.commit()

cursor.execute(
    """SELECT symbol ,name, id, market FROM stock WHERE market = 'US_EQUITY'"""
)
client = StockHistoricalDataClient(API_KEY, API_SECRET)
rows = cursor.fetchall()

symbols = [row[0] for row in rows]

stock_dict = {}
print(f"There are {len(symbols)} stocks available")
chunk_size = 200
# # barsets = api.get_barset()
for row in rows:
    symbol = row[0]
    stock_dict[symbol] = row[2]


for i in range(0, len(symbols), chunk_size):
    symbol_chunck = symbols[i : i + chunk_size]
    # no keys required for crypto data

    request_params = StockBarsRequest(
        symbol_or_symbols=symbol_chunck,
        timeframe=TimeFrame.Day,
        start=datetime(2023, 5, 1),
    )
    bars = client.get_stock_bars(request_params)
    try:
        for _symbol in symbol_chunck:
            bar = bars[_symbol]
            stock_id = stock_dict[_symbol]
            for entry in bar:
                cursor.execute(
                    """
                INSERT INTO stock_price (stock_id, date, open, high, low, close, volume, vwap)
                VALUES (?, ?,?,?,?,?,?, ?)
            """,
                    (
                        stock_id,
                        entry.timestamp.date().isoformat(),
                        entry.open,
                        entry.high,
                        entry.low,
                        entry.close,
                        entry.volume,
                        entry.vwap,
                    ),
                )
    except:
        print(_symbol)

    connection.commit()
