import warnings
import datetime
import pandas as pd
import yfinance as yf
import src.composer as composer
import src.utils as utils
from src.allocate import allocate, preprocess, price_history
from src.parse import parse

symponies = [
  'wzDUjTZQGeLFCD7nYA9d', # Test Stdevr
  'g9xMjPlQtnSzcINBaKgj', # Test MAR
  '2epuaVyiooe5wGVxs1Ps', # Test Stdev
  '87Sxtv9ZlYZfwVU7TwHq', # Test CR
  'gGpTJO2qpzfEAXHgWciX', # Test EMA
  'Fh0KTN40v0i6nCx26VWp', # Test MDD
]

# Fetch and print the JSON data
num_days = 10
date = datetime.date.today()

sub_algos = []
for symphony_id in symponies:
  data = composer.fetch_definition(symphony_id)
  if data is not None:
    sub_algos.append(parse(data))

switchboard = ['filter', sub_algos, ['stdevr', 5], ['top', 2]]

summary = preprocess(switchboard)
tickers = summary["assets"]

start_date = utils.subtract_trading_days(date, summary["max_window_days"] + num_days)
price_data = yf.download(" ".join(tickers), start=start_date, end=(date + datetime.timedelta(days=1)), progress=False)

range = price_data.index[-num_days:]
df = pd.DataFrame(0.0, index=range, columns=tuple(summary["investable_assets"]))

cache_data = {}
for r in range:
  allocation = allocate(switchboard, r, price_data, cache_data)
  for t in summary["investable_assets"]:
    df.at[r, t] = allocation[t]

print(df)
print(summary)