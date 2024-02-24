import warnings
import datetime
import pandas as pd
import yfinance as yf
import src.composer as composer
import src.utils as utils
from src.allocate import allocate, preprocess, price_history
from src.parse import parse

warnings.filterwarnings(
  "ignore",
  message="The 'unit' keyword in TimedeltaIndex construction is deprecated",
  category=FutureWarning,
  module="yfinance",
)

# Example symphony_id
# Example respomse
# https://app.composer.trade/symphony/wmDK13UrFbWbObhmnQLG/details
# https://codebeautify.org/jsonviewer/y24e1177e
symphony_id = (
  "wmDK13UrFbWbObhmnQLG"  # hwrdr - TQQQ For The Long Term (Reddit Post Link)
)

# Fetch and print the JSON data
num_days = 10
date = datetime.date.today()

data = composer.fetch_definition(symphony_id)
algo = parse(data)

summary = preprocess(algo)
tickers = summary["assets"]

start_date = utils.subtract_trading_days(date, summary["max_window_days"] + num_days)
price_data = yf.download(
  " ".join(tickers),
  start=start_date,
  end=(date + datetime.timedelta(days=1)),
  progress=False,
)

range = price_data.index[-num_days:]
df = pd.DataFrame(0.0, index=range, columns=tuple(summary["investable_assets"]))

cache_data = {}
for r in range:
  allocation = allocate(algo, r, price_data, cache_data)
  for t in summary["investable_assets"]:
    df.at[r, t] = allocation[t]

print(df)
print(summary)

print(price_history(algo, range[-1], num_days, price_data, cache_data))
