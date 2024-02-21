import datetime
import yfinance as yf
import src.utils as utils
from src.allocate import allocate, preprocess

# if current price of SPY is > 200d moving average of SPY, buy $SPY, otherwise buy $BIL
algo = ['ifelse',
  ['gt', ['now', ['asset', 'SPY']], ['ma', ['asset', 'SPY'], 200]]  ,
  ['asset', 'TQQQ'],
  ['asset', 'BIL']
]

# pick a trading day
date = datetime.date(2024, 2, 20)

# look up historical data data
price_data_start = utils.subtract_trading_days(date, 201) # need >= 200 days of data for SPY 200d MA
price_data_end = (date + datetime.timedelta(days=1))
price_data = yf.download("SPY TQQQ BIL", start=price_data_start, end=price_data_end, progress=False)

# get allocation for 2024-2-20
allocation = allocate(algo, date, price_data)

print(allocation)