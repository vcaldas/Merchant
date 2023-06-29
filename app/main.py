import os
import sqlite3
from datetime import date, timedelta

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")


load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    stock_filter = request.query_params.get("filter", False)

    connection = sqlite3.connect(os.getenv("LOCAL_DB"))
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    if stock_filter:
        if stock_filter == "new_intraday_highs":
            print("load")
            cursor.execute(
                """
                SELECT * FROM (
                SELECT symbol, name, stock_id, max(close), date FROM
                stock_price join stock on stock.id = stock_price.stock_id
                GROUP BY stock_id
                ORDER BY symbol )
                WHERE date = ?
            """,
                ((date.today() - timedelta(days=1)).isoformat(),),
            )

    else:
        cursor.execute("""SELECT id, symbol ,name from stock ORDER BY name""")

    rows = cursor.fetchall()
    return templates.TemplateResponse(
        "index.html", {"request": request, "stocks": rows}
    )


@app.get("/stock/{symbol}", response_class=HTMLResponse)
def stock_detail(request: Request, symbol):
    connection = sqlite3.connect(os.getenv("LOCAL_DB"))
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM strategy
    """
    )
    strategies = cursor.fetchall()

    cursor.execute(
        """
            SELECT id, symbol, name, exchange FROM stock WHERE symbol = ?
        """,
        (symbol,),
    )

    row = cursor.fetchone()

    cursor.execute(
        """
            SELECT * FROM stock_price WHERE stock_id = ?
            """,
        (row["id"],),
    )
    prices = cursor.fetchall()
    return templates.TemplateResponse(
        "stock_detail.html",
        {"request": request, "stock": row, "prices": prices, "strategies": strategies},
    )


@app.post("/apply_strategy")
def apply_strategy(strategy_id: int = Form(...), stock_id: int = Form(...)):
    connection = sqlite3.connect(os.getenv("LOCAL_DB"))
    cursor = connection.cursor()
    cursor.execute(
        """
            INSERT INTO stock_strategy (stock_id, strategy_id) VALUES (?,?)
            """,
        (
            stock_id,
            strategy_id,
        ),
    )

    connection.commit()
    return RedirectResponse(url=f"/strategy/{strategy_id}", status_code=303)


@app.get("/strategy/{strategy_id}")
def strategy(request: Request, strategy_id):
    connection = sqlite3.connect(os.getenv("LOCAL_DB"))
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
            SELECT id, name
            FROM strategy
            WHERE id= ?
            """,
        (strategy_id,),
    )

    strategy = cursor.fetchone()

    cursor.execute(
        """
            SELECT symbol, name
            FROM stock JOIN stock_strategy on stock_strategy.stock_id = stock.id
            WHERE strategy_id = ?
            """,
        (strategy_id,),
    )

    stocks = cursor.fetchall()

    return templates.TemplateResponse(
        "strategy.html", {"request": request, "stocks": stocks, "strategy": strategy}
    )
