# Classes
import sqlite3


class Best20:

    def get(self, index, strategy):
        conn = sqlite3.connect("db.db")
        cur = conn.cursor()
        cur.execute(f"""SELECT symbol, {strategy} FROM {index} ORDER BY
                       {strategy} DESC LIMIT 20""")
        result = cur.fetchall()
        return result


class Stock:

    def __init__(self, ticker):
        self.ticker = ticker
        self._momentum_12_1 = Momentum_12_1()
        self._momentum_12_2 = Momentum_12_2()
        self._ma10 = MA10()
        self._ep = EP()
        self._index = Index()

    def momentum_12_1(self):
        return self._momentum_12_1.get(self.ticker)

    def momentum_12_2(self):
        return self._momentum_12_2.get(self.ticker)

    def ma10(self):
        return self._ma10.get(self.ticker)

    def ep(self):
        return self._ep.get(self.ticker)

    def index(self):
        return self._index.get()


class Dj30:

    def __init__(self, strategy):
        self.strategy = strategy
        self._best20 = Best20()

    def best20(self):
        return self._best20.get('dj30', self.strategy)


class Sp500:

    def __init__(self):
        self._best20 = Best20()

    def best20(self, strategy):
        return self._best20.get('sp500', strategy)


class Divs:

    def __init__(self):
        self._best20 = Best20()

    def best20(self, strategy):
        return self._best20.get("divs", strategy)


class ETF:
    pass
