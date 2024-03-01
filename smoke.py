import warnings
import datetime
import pandas as pd
import yfinance as yf
import src.composer as composer
import src.utils as utils
from src.allocate import backtest, preprocess
from src.parse import parse

warnings.filterwarnings(
  "ignore",
  message="The 'unit' keyword in TimedeltaIndex construction is deprecated",
  category=FutureWarning,
  module="yfinance",
)

symponies = [
  # 'HhMTavgzaIbD7rh7LM5D',  # Too long to load. hwrdr - Master Switchboard
  "wmDK13UrFbWbObhmnQLG",  # Works
  "JgsHlLLVCwLBduSsxL4V",  # Works. hwrdr - TQQQ FTLT Original - JKoz Tweaked Copy - s/UVXY/VIXY
  "08Kfs9P7LYH5I0IYuDLf",  # Works
  "H9ORvJ20z0uk4wTVvRb1",  # Works
  "M3vczEzxMOH5YYzMU4PT",  # Works. WT Specific
  "wzDUjTZQGeLFCD7nYA9d",  # Works. Test Stdevr
  "g9xMjPlQtnSzcINBaKgj",  # Works. Test MAR
  "2epuaVyiooe5wGVxs1Ps",  # Works. Test Stdev
  "87Sxtv9ZlYZfwVU7TwHq",  # Works. Test CR
  "gGpTJO2qpzfEAXHgWciX",  # Works. Test EMA
  "Fh0KTN40v0i6nCx26VWp",  # Works. Test MDD
  "SqEr82qGXB3muOAa3g99",  # Works. Test Non-fracional Assets
  # "Wc26zCuOAQ3vXOXtAxor",  # 2024-02-12 chooses the wrong investment
]

# using "yesterday" to avoid getting intraday price data
# if this is called during market hours
yesterday = datetime.date.today() + datetime.timedelta(days=-1)
num_days = 15
cache_data = {}

for id in symponies:
  definition = composer.fetch_definition(id)
  algo = parse(definition)
  summary = preprocess(algo)

  tickers = summary["assets"]

  adjusted_start_date = utils.subtract_trading_days(
    yesterday, summary["max_window_days"] + num_days
  )

  # end is exclusive [start, end) so we need to add an extra day
  price_data = yf.download(
    " ".join(tickers),
    start=adjusted_start_date,
    end=(yesterday + datetime.timedelta(days=1)),
    progress=False,
  )

  print(f"{definition['id']} / {definition['name']}")

  range_start = price_data.index[0]
  range_end = price_data.index[-1]
  actual_start_date = price_data.index[-num_days]

  actuals = composer.fetch_backtest(id, actual_start_date, range_end)

  expected = pd.DataFrame().reindex_like(actuals)
  for col in actuals.columns:
    expected[col].values[:] = 0.0

  fractional = utils.alpaca_allows_fracional_shares_check(summary["investable_assets"])
  simulation = backtest(10000.0, algo, actual_start_date, range_end, price_data, cache_data, fractional)

  tickers = list(summary["investable_assets"]) + ["$USD"]
  for d, portfolio_value, daily_portfolio in simulation:
    for t in tickers:
      position = daily_portfolio.get(t, (0.0, 0.0, 0.0))
      ticker_allocation, purchase_prices, shares_owned = position
      expected.at[d, t] = ticker_allocation

  compare = expected.compare(actuals)

  print("Expected\n", expected, "\n")
  print("Actuals\n", actuals, "\n")
  print("Diff\n", compare, "\n")

  if not compare.empty:
    margin = 0.0021
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
          print(f"{d}: {ticker} delta {delta} was outside of the margin of error")
        elif delta > 0.0:
          print(f"{d}: {ticker} delta {delta} was within the margin of error")

    if not found:
      continue

    print("Issues found")
    exit()

print("No issues found")
