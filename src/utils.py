import datetime
import os
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass, AssetStatus

def subtract_trading_days(start_date, trading_days=10, fuzz=1.15):
  trading_days = int(float(trading_days) * fuzz)

  # Convert start_date to a datetime object if it's a string
  if isinstance(start_date, str):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")

  days_subtracted = 0
  while days_subtracted < trading_days:
    start_date -= datetime.timedelta(days=1)  # Move back one day
    if (
      start_date.weekday() < 5
    ):  # Monday to Friday are considered trading days (0 to 4)
      days_subtracted += 1

  return start_date


def alpaca_allows_fracional_shares_check(tickers):
  API_KEY = os.getenv("APCA_API_KEY_ID", "")
  API_SECRET = os.getenv('APCA_API_SECRET_KEY', "")

  client = TradingClient(API_KEY, API_SECRET, paper=True)

  results = {}

  request = GetAssetsRequest(
    asset_class=AssetClass.US_EQUITY,
    status=AssetStatus.ACTIVE
  )
  assets = client.get_all_assets(request)

  for asset in assets:
      if asset.symbol in tickers:
          results[asset.symbol] = asset.fractionable

  return results