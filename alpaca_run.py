import src.utils as utils

tickers = ['AAPL', 'GOOGL', 'MSFT', 'VIXY']  # Add your tickers here
fractional_shares_allowed = utils.alpaca_allows_fracional_shares_check(tickers)
print(fractional_shares_allowed)