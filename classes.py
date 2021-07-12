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
