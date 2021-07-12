import sys
import db.defs
from db.database import dj30, sp500, divs

index = sys.argv[1]
if index == 'dj30':
    dj30()
elif index == 'sp500':
    sp500()
elif index == 'divs':
    divs()
