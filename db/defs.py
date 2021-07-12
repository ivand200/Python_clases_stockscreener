import json
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import numpy as np
import yahoo_fin.stock_info as si
import urllib.request, urllib.parse, urllib.error

# Define previous month
now = datetime.now()
lastmonth = now - timedelta(weeks=5)
endoflastmonth = lastmonth.replace(day=28)
month_ago = endoflastmonth.strftime("%Y-%m-%d")
start_ = now - timedelta(weeks=120)
start_time = start_.strftime("%Y-%m-%d")


def shares_outstanding(ticker):
    """Get shares outstanding"""
    try:
        url = (f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=defaultKeyStatistics")
        fhand = urllib.request.urlopen(url).read()
        data = json.loads(fhand)
        return (data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["sharesOutstanding"]["raw"])
    except:
        return 0


def average_income(ticker):
    """Average income for last 4 years"""
    try:
        url = (f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=incomeStatementHistory")
        fhand = urllib.request.urlopen(url).read()
        data = json.loads(fhand)
        year1 = (data["quoteSummary"]["result"][0]["incomeStatementHistory"]["incomeStatementHistory"][0]["netIncome"]["raw"])
        year2 = (data["quoteSummary"]["result"][0]["incomeStatementHistory"]["incomeStatementHistory"][1]["netIncome"]["raw"])
        year3 = (data["quoteSummary"]["result"][0]["incomeStatementHistory"]["incomeStatementHistory"][2]["netIncome"]["raw"])
        year4 = (data["quoteSummary"]["result"][0]["incomeStatementHistory"]["incomeStatementHistory"][3]["netIncome"]["raw"])
    except:
        return 0
    else:
        return (year1 + year2 + year3 + year4) / 4


def get_close(ticker):
    """Get last close price"""
    try:
        url = (f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=price")
        fhand = urllib.request.urlopen(url).read()
        data = json.loads(fhand)
        return (data["quoteSummary"]["result"][0]["price"]["regularMarketPreviousClose"]["raw"])
    except:
        return 0



def get_ep(share):
    """E/P"""
    try:
        e_p = round(((average_income(share) / shares_outstanding(share))
                      / get_close(share)), 2)
    except:
        return 0
    else:
        return e_p



def get_momentum_12_1(share):
    """Get Momentum_12_1"""
    try:
        ticker = yf.Ticker(share)
        ticker = ticker.history(start=start_time, end=month_ago, interval="1mo")
        ticker = ticker[ticker["Close"].notna()]
        ticker["Price0"] = ticker["Close"].shift(12)
        ticker["Price1"] = ticker["Close"]
        ticker["mom_12"] = (ticker["Price1"] / ticker["Price0"]) - 1
    except:
        return 0
    else:
        return round(ticker["mom_12"][-1], 2)


def get_ma10(share):
    """Last close price compare to MA10, 1 = close price higher than MA10"""
    try:
        ticker = yf.Ticker(share)
        ticker = ticker.history(start=start_time, end=month_ago, interval="1mo")
        ticker = ticker[ticker["Close"].notna()]
        ticker["MA10"] = ticker["Close"].rolling(10).mean()
        ticker["Difference"] = (ticker["Close"] / ticker["MA10"]) - 1
        ticker["Direction"] = [1 if ticker.loc[ei, "Difference"] > 0 else -1 for ei in ticker.index]
        result = ticker["Direction"][-1]
    except:
        return 0
    else:
        return int(result)


def get_momentum_12_2(ticker):
    """Get Momentum_12_2"""
    try:
        ticker = si.get_data(f"{ticker}", start_date =start_time, end_date = month_ago, interval = '1mo')
        ticker = ticker[ticker["close"].notna()]
        ticker["Price0"] = ticker["close"].shift(12)
        ticker["Price1"] = ticker["close"].shift(1)
        ticker["mom_12_1"] = (ticker["Price1"] / ticker["Price0"]) - 1
    except:
        return 0
    else:
        return (round(ticker["mom_12_1"][-1], 2))


def get_div(share):
    """Dividend average for last 5 years / last close price"""
    try:
        div = si.get_dividends(share)['dividend'][-20:].mean()
        div_income = (div * 4) / get_close(share)
    except:
        return 0
    else:
        return round(div_income, 3)


def get_avg_momentum(share):
    """Get AVG Momentum(12, 6, 3)"""
    try:
        ticker = yf.Ticker(share)
        ticker = ticker.history(start=start_time, end=month_ago, interval="1mo")
        ticker = ticker[ticker["Close"].notna()]
        ticker['Close0'] = ticker['Close'].shift(12)
        ticker['Close1'] = ticker['Close'].shift(6)
        ticker['Close2'] = ticker['Close'].shift(3)
        ticker['Mom_0'] = ((ticker['Close'] / ticker['Close0']) - 1) * 0.33
        ticker['Mom_1'] = ((ticker['Close'] / ticker['Close1']) - 1) * 0.33
        ticker['Mom_2'] = ((ticker['Close'] / ticker['Close2']) - 1) * 0.33
        ticker['Avg_Mom'] = ticker['Mom_0'] + ticker['Mom_1'] + ticker['Mom_2']
    except:
        return 0
    else:
        return round(ticker['Avg_Mom'][-1], 2)
