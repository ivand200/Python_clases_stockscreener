from classes import Dj30, Sp500, Divs
import click

@click.command()
@click.option('-ticker', help='ticker')
@click.option('-strategy', prompt='Enter strategy', help='strategy')


def _main(ticker, strategy):
    try:
        if ticker == "dj30":
            ticker = Dj30(strategy)
            result = ticker.best20()
            print(result)
        elif ticker == "sp500":
            ticker = Sp500()
            result = ticker.best20(strategy)
            print(result)
        elif ticker == 'divs':
            ticker = Divs()
            result = ticker.best20(strategy)
            print(result)
        else:
             print("Wrong if")
    except:
        print("Wrong")


if __name__ == "__main__":
    _main()
