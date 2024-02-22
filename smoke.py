import warnings
import datetime
import pandas as pd
import yfinance as yf
import src.composer as composer
import src.utils as utils
from src.allocate import allocate, preprocess
from src.parse import parse

warnings.filterwarnings(
    "ignore",
    message="The 'unit' keyword in TimedeltaIndex construction is deprecated",
    category=FutureWarning,
    module="yfinance",
)

symponies = [
  #'HhMTavgzaIbD7rh7LM5D', # hwrdr - Master Switchboard
  'wmDK13UrFbWbObhmnQLG',
  'JgsHlLLVCwLBduSsxL4V', # hwrdr - TQQQ FTLT Original - JKoz Tweaked Copy - s/UVXY/VIXY
  '08Kfs9P7LYH5I0IYuDLf',
  'H9ORvJ20z0uk4wTVvRb1',
  'M3vczEzxMOH5YYzMU4PT', # WT Specific
  'wzDUjTZQGeLFCD7nYA9d', # Test Stdevr
  'g9xMjPlQtnSzcINBaKgj', # Test MAR
  '2epuaVyiooe5wGVxs1Ps', # Test Stdev
  '87Sxtv9ZlYZfwVU7TwHq', # Test CR
  'gGpTJO2qpzfEAXHgWciX', # Test EMA
  'Fh0KTN40v0i6nCx26VWp', # Test MDD
  'Wc26zCuOAQ3vXOXtAxor'
]

today = datetime.date.today()
num_days = 10
cache_data = {}

for id in symponies:

  definition = composer.fetch_definition(id)
  algo = parse(definition)
  summary = preprocess(algo)

  tickers = summary["assets"]

  adjusted_start_date = utils.subtract_trading_days(today, summary["max_window_days"] + num_days)

  # end is exclusive [start, end) so we need to add an extra day
  price_data = yf.download(" ".join(tickers), start=adjusted_start_date, end=(today + datetime.timedelta(days=1)), progress=False)

  print(f"{definition['id']} / {definition['name']}")

  range_start = price_data.index[0]
  actual_start_date = price_data.index[-num_days]

  actuals = composer.fetch_backtest(id, actual_start_date, today)

  date_range = pd.date_range(start=actual_start_date, end=today)
  expected = pd.DataFrame().reindex_like(actuals)
  for col in actuals.columns:
    expected[col].values[:] = 0.0

  for trading_date in price_data.index[-num_days:]:
    allocation = allocate(algo, trading_date, price_data, cache_data)

    for t in summary["investable_assets"]:
      expected.at[trading_date, t] = allocation[t]

  compare = expected.compare(actuals)

  print("Expected\n", expected, "\n")
  print("Actuals\n", actuals, "\n")
  print("Diff\n", compare, "\n")

  if not compare.empty:
    if ("$USD", "other") in compare.columns and compare["$USD"]["other"].iloc[0] > 0:
      total = 0.0
      for ticker, table in compare.columns:
        if table == "self" and ticker != "$USD":
          total = total + compare[ticker]["self"].iloc[0]

      if compare["$USD"]["other"].iloc[0] != (1.0 - total):
        continue

    margin = 0.002
    found = False
    for d in compare.index:
      size = int(len(compare.columns) / 2)
      for idx in range(0, size):
        ticker = compare.columns[idx * 2][0]

        self_val = compare[ticker]["self"][d]
        other_val = compare[ticker]["other"][d]

        delta = abs(self_val - other_val)
        if delta >= margin:
          found = True
          print(f"Delta {delta} was outside of the margin of error")
        elif delta > 0.0:
          print(f"Delta {delta} was within the margin of error")

    if not found:
      continue

    print("Issues found")
    exit()

print("No issues found")






