from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import sqlite3
import os
from dotenv import load_dotenv
templates = Jinja2Templates(directory="app/templates")


load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    connection = sqlite3.connect(os.getenv('LOCAL_DB'))
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT id, symbol ,name from stock ORDER BY name""")

    rows = cursor.fetchall()
    return templates.TemplateResponse("index.html", {'request': request, "stocks": rows})


@app.get("/stock/{symbol}", response_class=HTMLResponse)
def stock_detail(request: Request, symbol):
    connection = sqlite3.connect(os.getenv('LOCAL_DB'))
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(
        """
            SELECT id, symbol, name FROM stock WHERE symbol = ?
        """, (symbol,))

    row = cursor.fetchone()

    cursor.execute("""
            SELECT * FROM stock_price WHERE stock_id = ?
            """, (row['id'],))
    prices = cursor.fetchall()
    return templates.TemplateResponse("stock_detail.html", {'request': request, "stock": row, "prices": prices})
