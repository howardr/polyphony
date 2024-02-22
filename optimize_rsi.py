import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import yfinance as yf
import src.utils as utils
from itertools import product
import matplotlib.pyplot as plt
from src.allocate import allocate, cr, preprocess, price_history

def generate_algo(days, gt_rsi_percent):
  tqqq_or_not = ['ifelse',
    ['gt', ['now', ['asset', 'SPY']], ['ma', ['asset', 'SPY'], 200]],

    # bull market
    ['asset', 'TQQQ'],

    # bear market
    ['asset', 'BIL'] 
  ]

  overbought_wrapper = ['ifelse',
    ['gt', ['rsi', ['asset', 'SPY'], days], ['number', gt_rsi_percent]],
    ['asset', 'BIL'],
    tqqq_or_not
  ]

  return overbought_wrapper

date = datetime.date(2024, 2, 20)
num_days = 500
days = range(10, 60)
rsi_percents = range(59, 80)
combs = list(product(days, rsi_percents))

algos = []
max_window_days = 0
summary = None
for days, rsi_percent in combs:
  algo = generate_algo(days, rsi_percent)
  summary = preprocess(algo)
  max_window_days = max(max_window_days, summary["max_window_days"])
  algos.append(algo)

tickers = summary["assets"]

price_start_date = utils.subtract_trading_days(date, max_window_days + num_days)
price_data = yf.download(" ".join(tickers), start=price_start_date, end=(date + datetime.timedelta(days=1)), progress=False)

runs = zip(algos, combs)
comb_stats = []
cache_data = {}
for algo, (days, gt_rsi_percent) in runs:
  pct_return = cr(algo, pd.to_datetime(date), num_days, price_data, cache_data=cache_data)
  comb_stats.append((days, gt_rsi_percent, pct_return))

  print(f"Days: {days}, GT RSI Percent: {gt_rsi_percent}, Percent Return: {pct_return}")

# Convert list of tuples into a DataFrame
df = pd.DataFrame(comb_stats, columns=['days', 'gt_rsi_percent', 'pct_return'])

# Correctly pivot the DataFrame
pivot_table = df.pivot(index='days', columns='gt_rsi_percent', values='pct_return')

# Plotting the heatmap
sns.heatmap(pivot_table, cmap='viridis', annot=True)
plt.title('Percent Returns Heatmap')
plt.xlabel('GT RSI Percent')
plt.ylabel('RSI Days')
plt.show()