import datetime
import random
import requests
import yfinance as yf
from src.parse import parse
from src.allocate import allocate, preprocess
import pandas as pd
import sys

def fetch_and_parse_json(symphony_id):
  url = f"https://backtest-api.composer.trade/api/v1/public/symphonies/{symphony_id}/score"
  response = requests.get(url)
  
  if response.status_code == 200:
    # Parse JSON response into Python dictionary
    data = response.json()
    return data
  else:
    print(f"Failed to fetch data: HTTP {response.status_code}")
    return None

def subtract_trading_days(start_date, trading_days=10):
  trading_days = int(float(trading_days) * 1.1)

  # Convert start_date to a datetime object if it's a string
  if isinstance(start_date, str):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
  
  days_subtracted = 0
  while days_subtracted < trading_days:
    start_date -= datetime.timedelta(days=1)  # Move back one day
    if start_date.weekday() < 5:  # Monday to Friday are considered trading days (0 to 4)
      days_subtracted += 1

  return start_date

# Example symphony_id
# Example respomse
# https://app.composer.trade/symphony/wmDK13UrFbWbObhmnQLG/details
# https://codebeautify.org/jsonviewer/y24e1177e
symphony_id = 'HhMTavgzaIbD7rh7LM5D'  #
symphony_id = 'wmDK13UrFbWbObhmnQLG'

symphony_id = 'JgsHlLLVCwLBduSsxL4V' # hwrdr - TQQQ FTLT Original - JKoz Tweaked Copy - s/UVXY/VIXY
symphony_id = '08Kfs9P7LYH5I0IYuDLf'
symphony_id = 'H9ORvJ20z0uk4wTVvRb1'
symphony_id = 'M3vczEzxMOH5YYzMU4PT' # WT Specific
symphony_id = 'wzDUjTZQGeLFCD7nYA9d' # Test Stdevr
symphony_id = 'g9xMjPlQtnSzcINBaKgj' # Test MAR
symphony_id = '2epuaVyiooe5wGVxs1Ps' # Test Stdev
symphony_id = '87Sxtv9ZlYZfwVU7TwHq' # Test CR
symphony_id = 'gGpTJO2qpzfEAXHgWciX' # Test EMA
symphony_id = 'Fh0KTN40v0i6nCx26VWp' # Test MDD
symphony_id = 'Wc26zCuOAQ3vXOXtAxor'
#symphony_id = 'A359IqvhQ4Ice2QaWacZ'

# Fetch and print the JSON data
data = None
algo = None
num_days = 1
date = datetime.date(2024, 2, 20)

data = fetch_and_parse_json(symphony_id)


if data is not None:
  print(data)
  algo = parse(data)

# # Test
# # https://app.composer.trade/symphony/Rcwkb8bt8501lAaduqsz/details
# # vs
# algo = ["wteq", [
#     ["ifelse",
#      ["gt", ["now", ["asset", "SPY"]], ["ma", ["asset", "SPY"], 200]],
#      ["asset", "TQQQ"],
#      ["asset", "BIL"]
#     ]
#   ]]

# # Test
# # https://app.composer.trade/symphony/rrkugCKc0HW4WpnPZegx/details
# # vs
# algo = ["wteq", [
#     ["ifelse",
#      ["gt", ["rsi", ["asset", "SPY"], 10], ["number", 60]],
#      ["asset", "BIL"],
#      ["asset", "TQQQ"]
#     ]
#   ]]

#algo = ('group', 'V1 BWC SPY Volatility Focus ? Anti-Beta ? Low Correlation ', ('wteq', (('wteq', (('ifelse', ('gt', ('now', ('asset', 'SPY')), ('ma', ('asset', 'SPY'), 50)), ('wteq', (('ifelse', ('lt', ('rsi', ('asset', 'SPY'), 5), ('number', 35.0)), ('asset', 'SVIX'), ('wteq', (('ifelse', ('gt', ('rsi', ('asset', 'SPY'), 10), ('number', 65.0)), ('wteq', (('ifelse', ('lt', ('cr', ('asset', 'SPY'), 3), ('number', 0.0)), ('wteq', (('filter', (('asset', 'UVXY'), ('asset', 'VIXM'), ('asset', 'VXZ'), ('asset', 'VXX')), ('mar', 5), ('bottom', 1)),)), ('wteq', (('filter', (('asset', 'VXX'), ('asset', 'BTAL')), ('rsi', 2), ('top', 1)),))),)), ('wteq', (('ifelse', ('gt', ('ema', ('asset', 'SPY'), 2), ('ema', ('asset', 'SPY'), 5)), ('asset', 'SVIX'), ('wteq', (('filter', (('asset', 'BTAL'), ('asset', 'BIL'), ('asset', 'GLD'), ('asset', 'XLE'), ('asset', 'COM'), ('asset', 'SHV')), ('mar', 10), ('top', 2)), ('asset', 'BTAL')))),))),))),)), ('wteq', (('filter', (('asset', 'BTAL'), ('asset', 'BTAL'), ('asset', 'BIL'), ('asset', 'GLD'), ('asset', 'XLE'), ('asset', 'COM'), ('asset', 'SHV')), ('mar', 30), ('top', 3)),))),)),))), ('asset', 'VXX'), ('asset', 'KMLM'), ('filter', (('asset', 'DBMF'), ('asset', 'KMLM'), ('asset', 'FMF'), ('asset', 'CTA'), ('asset', 'WTMF')), ('rsi', 14), ('bottom', 1)), ('asset', 'BTAL'), ('asset', 'TECL'), ('asset', 'GLD'), ('asset', 'COM'), ('asset', 'XLE'), ('asset', 'VIXM'), ('asset', 'SPXL'), ('asset', 'WTMF'), ('asset', 'SVXY'), ('asset', 'SHY'), ('group', 'V3 BWC: Managed Futures', ('wteq', (('wteq', (('wtinvol', (('filter', (('asset', 'DBMF'), ('asset', 'KMLM'), ('asset', 'FMF'), ('asset', 'CTA'), ('asset', 'WTMF')), ('stdevr', 20), ('bottom', 1)), ('filter', (('asset', 'DBMF'), ('asset', 'KMLM'), ('asset', 'FMF'), ('asset', 'CTA'), ('asset', 'WTMF')), ('rsi', 10), ('bottom', 1)), ('filter', (('asset', 'DBMF'), ('asset', 'KMLM'), ('asset', 'FMF'), ('asset', 'CTA'), ('asset', 'WTMF')), ('mdd', 20), ('bottom', 1)), ('filter', (('asset', 'DBMF'), ('asset', 'KMLM'), ('asset', 'FMF'), ('asset', 'CTA'), ('asset', 'WTMF')), ('rsi', 14), ('bottom', 1))), 20),)),))), ('asset', 'BIL'), ('asset', 'SHV'), ('filter', (('asset', 'DBMF'), ('asset', 'KMLM'), ('asset', 'FMF'), ('asset', 'CTA'), ('asset', 'WTMF')), ('mdd', 20), ('bottom', 1)), ('filter', (('asset', 'DBMF'), ('asset', 'KMLM'), ('asset', 'FMF'), ('asset', 'CTA'), ('asset', 'WTMF')), ('rsi', 10), ('bottom', 1)), ('asset', 'CTA'), ('asset', 'VXZ'), ('asset', 'FMF'), ('asset', 'TLT'), ('asset', 'BSV'), ('asset', 'DBMF'), ('asset', 'UVXY'), ('filter', (('asset', 'DBMF'), ('asset', 'KMLM'), ('asset', 'FMF'), ('asset', 'CTA'), ('asset', 'WTMF')), ('stdevr', 20), ('bottom', 1))
#algo = ('group', '35D StdDev Top 2', ('wteq', (('wteq', (('filter', (('group', 'Zero Beta Dividends - 8 Feb 2018 (USDU- "perfect RSI numbers" 1 off to "unsafe" side) AR 73.6% - DD 8.7% Beta -0.10', ('wteq', (('wteq', (('group', 'Single Popped Dividends (UVXY)', ('wteq', (('wteq', (('ifelse', ('gt', ('rsi', ('asset', 'QQQ'), 10), ('number', 81.0)), ('group', 'UVXY', ('wteq', (('wteq', (('asset', 'UVXY'), ('asset', 'TMF'))),))), ('wteq', (('ifelse', ('gt', ('rsi', ('asset', 'VTV'), 10), ('number', 77.0)), ('group', 'UVXY', ('wteq', (('wteq', (('asset', 'UVXY'), ('asset', 'TMF'))),))), ('wteq', (('ifelse', ('gt', ('rsi', ('asset', 'VOOG'), 10), ('number', 77.0)), ('group', 'UVXY', ('wteq', (('wteq', (('asset', 'UVXY'), ('asset', 'TMF'))),))), ('wteq', (('ifelse', ('gt', ('rsi', ('asset', 'VOOV'), 10), ('number', 80.0)), ('group', 'UVXY', ('wteq', (('wteq', (('asset', 'UVXY'), ('asset', 'TMF'))),))), ('wteq', (('ifelse', ('gt', ('rsi', ('asset', 'XLP'), 10), ('number', 78.0)), ('group', 'UVXY', ('wteq', (('wteq', (('asset', 'UVXY'), ('asset', 'TMF'))),))), ('wteq', (('ifelse', ('gt', ('rsi', ('asset', 'XLY'), 10), ('number', 80.0)), ('group', 'UVXY', ('wteq', (('wteq', (('asset', 'UVXY'), ('asset', 'TMF'))),))), ('wteq', (('ifelse', ('gt', ('rsi', ('asset', 'SPY'), 10), ('number', 77.0)), ('group', 'UVXY', ('wteq', (('wteq', (('asset', 'UVXY'), ('asset', 'TMF'))),))), ('wteq', (('group', 'BSC', ('wteq', (('wteq', (('ifelse', ('gt', ('rsi', ('asset', 'UVXY'), 21), ('number', 65.0)), ('wteq', (('group', 'BSC', ('wteq', (('wteq', (('filter', (('asset', 'TLT'), ('asset', 'VIXM'), ('asset', 'SHY'), ('asset', 'GLD')), ('rsi', 21), ('top', 3)),)),))),)), ('wteq', (('group', 'Pop Up', ('wteq', (('wteq', (('ifelse', ('lt', ('rsi', ('asset', 'XLK'), 10), ('number', 30.0)), ('group', 'TECL', ('wteq', (('wteq', (('filter', (('asset', 'TECL'), ('asset', 'BSV')), ('rsi', 10), ('bottom', 1)), ('filter', (('asset', 'TECL'), ('asset', 'SVXY')), ('rsi', 10), ('top', 1)))),))), ('wteq', (('ifelse', ('lt', ('rsi', ('asset', 'QQQ'), 10), ('number', 30.0)), ('group', 'TECL', ('wteq', (('wteq', (('filter', (('asset', 'TECL'), ('asset', 'BSV')), ('rsi', 10), ('bottom', 1)), ('filter', (('asset', 'TECL'), ('asset', 'SVXY')), ('rsi', 10), ('top', 1)))),))), ('wteq', (('ifelse', ('lt', ('rsi', ('asset', 'SPY'), 10), ('number', 31.0)), ('group', 'SPXL', ('wteq', (('wteq', (('filter', (('asset', 'SPXL'), ('asset', 'BSV')), ('rsi', 10), ('bottom', 1)), ('filter', (('asset', 'SPXL'), ('asset', 'SVXY')), ('rsi', 10), ('top', 1)))),))), ('wteq', (('group', 'E', ('wteq', (('wteq', (('asset', 'SVXY'), ('asset', 'VIXM'), ('asset', 'BTAL'), ('asset', 'SCHD'))),))),))),))),))),)),))),))),)),))),))),))),))),))),))),))),))),)),))), ('group', 'Safety Town l A', ('wteq', (('wteq', (('ifelse', ('gte', ('rsi', ('asset', 'SPY'), 10), ('number', 70.0)), ('wteq', (('asset', 'VIXM'), ('asset', 'UVXY'))), ('wteq', (('group', 'A', ('wteq', (('wteq', (('filter', (('asset', 'SVXY'), ('asset', 'VIXM'), ('asset', 'BTAL')), ('stdev', 21), ('top', 2)),)),))),))),)),))))),))), ('group', 'V3 BWC: Managed Futures', ('wteq', (('wteq', (('wtinvol', (('filter', (('asset', 'DBMF'), ('asset', 'KMLM'), ('asset', 'FMF'), ('asset', 'CTA'), ('asset', 'WTMF')), ('stdevr', 20), ('bottom', 1)), ('filter', (('asset', 'DBMF'), ('asset', 'KMLM'), ('asset', 'FMF'), ('asset', 'CTA'), ('asset', 'WTMF')), ('rsi', 10), ('bottom', 1)), ('filter', (('asset', 'DBMF'), ('asset', 'KMLM'), ('asset', 'FMF'), ('asset', 'CTA'), ('asset', 'WTMF')), ('mdd', 20), ('bottom', 1)), ('filter', (('asset', 'DBMF'), ('asset', 'KMLM'), ('asset', 'FMF'), ('asset', 'CTA'), ('asset', 'WTMF')), ('rsi', 14), ('bottom', 1))), 20),)),))), ('group', 'V1 BWC SPY Volatility Focus ? Anti-Beta ? Low Correlation ', ('wteq', (('wteq', (('ifelse', ('gt', ('now', ('asset', 'SPY')), ('ma', ('asset', 'SPY'), 50)), ('wteq', (('ifelse', ('lt', ('rsi', ('asset', 'SPY'), 5), ('number', 35.0)), ('asset', 'SVIX'), ('wteq', (('ifelse', ('gt', ('rsi', ('asset', 'SPY'), 10), ('number', 65.0)), ('wteq', (('ifelse', ('lt', ('cr', ('asset', 'SPY'), 3), ('number', 0.0)), ('wteq', (('filter', (('asset', 'UVXY'), ('asset', 'VIXM'), ('asset', 'VXZ'), ('asset', 'VXX')), ('mar', 5), ('bottom', 1)),)), ('wteq', (('filter', (('asset', 'VXX'), ('asset', 'BTAL')), ('rsi', 2), ('top', 1)),))),)), ('wteq', (('ifelse', ('gt', ('ema', ('asset', 'SPY'), 2), ('ema', ('asset', 'SPY'), 5)), ('asset', 'SVIX'), ('wteq', (('filter', (('asset', 'BTAL'), ('asset', 'BIL'), ('asset', 'GLD'), ('asset', 'XLE'), ('asset', 'COM'), ('asset', 'SHV')), ('mar', 10), ('top', 2)), ('asset', 'BTAL')))),))),))),)), ('wteq', (('filter', (('asset', 'BTAL'), ('asset', 'BTAL'), ('asset', 'BIL'), ('asset', 'GLD'), ('asset', 'XLE'), ('asset', 'COM'), ('asset', 'SHV')), ('mar', 30), ('top', 3)),))),)),)))), ('stdevr', 35), ('top', 2)),)),)))

summary = preprocess(algo)

# fetch trading data
uniq_tickers = summary["assets"]

start_date = subtract_trading_days(date, summary["max_window_days"] + num_days)
# end is exclusive [start, end) so we need to add an extra day
price_data = yf.download(" ".join(uniq_tickers), start=start_date, end=(date + datetime.timedelta(days=1)))

range_end = price_data.index[-1]



print("\t".join(summary["investable_assets"]))

#sys.setrecursionlimit(10000)

#exit()
cache_data = {}
for r in price_data.index[-num_days:]:
  allocation = allocate(algo, r, price_data, cache_data)
  row = [str(r.date())]
  for t in summary["investable_assets"]:
    if t in allocation:
      row.append(allocation[t])
    else:
      row.append(0)

  print("\t".join(map(str, row)))

print(summary)