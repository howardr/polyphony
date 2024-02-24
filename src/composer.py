import datetime
import pandas as pd
import requests


def fetch_definition(id):
  url = f"https://backtest-api.composer.trade/api/v1/public/symphonies/{id}/score"
  response = requests.get(url)

  if response.status_code == 200:
    # Parse JSON response into Python dictionary
    data = response.json()
    return data
  else:
    print(f"Failed to fetch data: HTTP {response.status_code}")
    return None


def fetch_backtest(id, start_date, end_date):
  payload = {
    "capital": 10000,
    "apply_reg_fee": True,
    "apply_taf_fee": True,
    "backtest_version": "v2",
    "slippage_percent": 0.0005,
    "start_date": start_date.strftime("%Y-%m-%d"),
    "end_date": end_date.strftime("%Y-%m-%d"),
  }

  url = f"https://backtest-api.composer.trade/api/v2/public/symphonies/{id}/backtest"

  data = requests.post(url, json=payload)
  jsond = data.json()

  holdings = jsond["last_market_days_holdings"]

  tickers = []
  for ticker in holdings:
    tickers.append(ticker)

  # Example format
  # {
  #   // key: ticker
  #   "SPY": {
  #     // key: days since linux epoch
  #     // value: percent allocation of ticker on date
  #     "19416": 0.123
  #   }
  # }
  allocations = jsond["tdvm_weights"]
  date_range = pd.date_range(start=start_date, end=end_date)
  df = pd.DataFrame(0.0, index=date_range, columns=tickers)

  for ticker in allocations:
    for date_int in allocations[ticker]:
      trading_date = convert_trading_date(date_int)
      percent = allocations[ticker][date_int]

      df.at[trading_date, ticker] = percent

  return df


def convert_trading_date(date_int):
  date_1 = datetime.datetime.strptime("01/01/1970", "%m/%d/%Y")
  dt = date_1 + datetime.timedelta(days=int(date_int))

  return dt
