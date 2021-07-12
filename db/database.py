import sqlite3
import json
import csv
import json
from db import defs


conn = sqlite3.connect("db/db.db")
cur = conn.cursor()


def dj30():
    cur.execute("""DROP TABLE IF EXISTS dj30""")
    cur.execute("""CREATE TABLE dj30 (id INTEGER NOT NULL PRIMARY KEY
                   AUTOINCREMENT UNIQUE, symbol TEXT, name TEXT, momentum_12_1 REAL,
                   momentum_12_2 REAL, MA10 INTEGER, ep REAL)""")

    with open('db/DJ30.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            symbol = row[1]
            name = row[0]
            momentum_12_1 = defs.get_momentum_12_1(row[1])
            momentum_12_2 = defs.get_momentum_12_2(row[1])
            ma10 = defs.get_ma10(row[1])
            ep = defs.get_ep(row[1])

            cur.execute("""INSERT INTO dj30 (symbol, name, momentum_12_1,
                   momentum_12_2, ma10, ep) VALUES (?, ?, ?, ?, ?, ?)""",
                   (symbol, name, momentum_12_1, momentum_12_2, ma10, ep))
            conn.commit()

        sqlstr = """SELECT symbol, momentum_12_1, momentum_12_2, ma10, ep FROM dj30
                ORDER BY momentum_12_2 DESC LIMIT 10"""
        for row in cur.execute(sqlstr):
            print(row[0], row[1], row[2], row[3], row[4])

        cur.close()


def sp500():
    cur.execute("""DROP TABLE IF EXISTS sp500""")
    cur.execute("""CREATE TABLE sp500 (id INTEGER NOT NULL PRIMARY KEY
                   AUTOINCREMENT UNIQUE, symbol TEXT, name TEXT, momentum_12_1 REAL,
                   momentum_12_2 REAL, MA10 INTEGER, ep REAL)""")

    with open("db/SP500_components_raw.json", "r") as f:
        file = f.read()
    data = json.loads(file)
    for item in data:
        symbol = item["Symbol"]
        name = item["Name"]
        momentum_12_1 = defs.get_momentum_12_1(item["Symbol"])
        momentum_12_2 = defs.get_momentum_12_2(item["Symbol"])
        ma10 = defs.get_ma10(item["Symbol"])
        ep = defs.get_ep(item["Symbol"])

        cur.execute("""INSERT INTO sp500 (symbol, name, momentum_12_1,
               momentum_12_2, ma10, ep) VALUES (?, ?, ?, ?, ?, ?)""",
               (symbol, name, momentum_12_1, momentum_12_2, ma10, ep))
        conn.commit()

    sqlstr = """SELECT symbol, momentum_12_1, momentum_12_2, ma10, ep FROM sp500
                ORDER BY momentum_12_2 DESC LIMIT 20"""
    for row in cur.execute(sqlstr):
        print(row[0], row[1], row[2], row[3], row[4])

    cur.close()


def divs():
    cur.execute("""DROP TABLE IF EXISTS divs""")
    cur.execute("""CREATE TABLE divs (id INTEGER NOT NULL PRIMARY KEY
                   AUTOINCREMENT UNIQUE, symbol TEXT, name TEXT, div_p REAL)""")

    with open('db/dividend_aristocrats.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            symbol = row[1]
            name = row[0]
            div_p = defs.get_div(row[1])

            cur.execute("""INSERT INTO divs (symbol, name, div_p)
                       VALUES (?, ?, ?)""", (symbol, name, div_p))
            conn.commit()

        sqlstr = """SELECT symbol, div_p FROM divs ORDER BY div_p DESC LIMIT 20"""

        for row in cur.execute(sqlstr):
            print(row[0], row[1])

        cur.close()
