import datetime

def subtract_trading_days(start_date, trading_days=10, fuzz=1.1):
  trading_days = int(float(trading_days) * fuzz)

  # Convert start_date to a datetime object if it's a string
  if isinstance(start_date, str):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
  
  days_subtracted = 0
  while days_subtracted < trading_days:
    start_date -= datetime.timedelta(days=1)  # Move back one day
    if start_date.weekday() < 5:  # Monday to Friday are considered trading days (0 to 4)
      days_subtracted += 1

  return start_date