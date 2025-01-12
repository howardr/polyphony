import pandas as pd
import pandas_ta as ta
from collections import defaultdict


def allocate(block, date, price_data, cache_data=None, fractional=None):
  if cache_data is None:
    cache_data = {}

  block_type = block[0]
  match block_type:
    case "asset":
      ticker = block[1]
      return {
        ticker: 1.0,
      }
    case "wteq" | "wtspec" | "wtinvol":
      blocks = block[1]

      weights = None
      match block_type:
        case "wtspec":
          weights = block[2]
        case "wteq":
          weights = []
          for i in range(0, len(blocks)):
            weights.append((1, len(blocks)))
        case "wtinvol":
          window_days = block[2]
          weights = []
          total = 0
          for b in blocks:
            invol = 1 / stdevr(b, date, window_days, price_data, cache_data, fractional, 10000.0)
            weights.append(invol)
            total = total + invol
          weights = tuple(map(lambda invol: (invol, total), weights))

      weighted_allocation = defaultdict(float)
      for i, b in enumerate(blocks):
        num, den = weights[i]
        wt = num / den
        for ticker, inner_wt in allocate(b, date, price_data, cache_data, fractional).items():
          weighted_allocation[ticker] = weighted_allocation[ticker] + (inner_wt * wt)

      return weighted_allocation
    case "ifelse":
      comparator = block[1]
      true_block = block[2]
      false_block = block[3]

      eval_block = None
      if run_comparator(comparator, date, price_data, cache_data, fractional):
        eval_block = true_block
      else:
        eval_block = false_block

      return allocate(eval_block, date, price_data, cache_data, fractional)
    case "filter":
      blocks = block[1]
      sort_indicator = block[2]
      select = block[3]

      values = []

      # some indicators will need an initial value and others won't. There are 2 cases
      # * Sorts over price and should not have an initial value as closing price should be used
      # * Sorts over return should have an initial value
      initial_value = 10000.0

      sort_indicator_op = sort_indicator[0]
      match sort_indicator_op:
        case "cr":
          window_days = sort_indicator[1]
          for b in blocks:
            values.append(cr(b, date, window_days, price_data, cache_data, fractional, initial_value))
        case "ema":
          window_days = sort_indicator[1]
          for b in blocks:
            values.append(ema(b, date, window_days, price_data, cache_data, fractional, use_fractional_if_provided=False))
        case "ma":
          window_days = sort_indicator[1]
          for b in blocks:
            values.append(ma(b, date, window_days, price_data, cache_data, fractional, use_fractional_if_provided=False))
        case "mar":
          window_days = sort_indicator[1]
          for b in blocks:
            values.append(mar(b, date, window_days, price_data, cache_data, fractional, initial_value))
        case "mdd":
          window_days = sort_indicator[1]
          for b in blocks:
            values.append(mdd(b, date, window_days, price_data, cache_data, fractional, initial_value))
        case "rsi":
          window_days = sort_indicator[1]
          for b in blocks:
            values.append(rsi(b, date, window_days, price_data, cache_data, fractional, initial_value))
        case "stdev":
          window_days = sort_indicator[1]
          for b in blocks:
            values.append(stdev(b, date, window_days, price_data, cache_data, fractional, use_fractional_if_provided=False))
        case "stdevr":
          window_days = sort_indicator[1]
          for b in blocks:
            values.append(stdevr(b, date, window_days, price_data, cache_data, fractional, initial_value))
        case _:
          raise ValueError(f"'{sort_indicator_op}' is not a defined filter sort")

      select_direction = select[0]
      select_limit = select[1]

      reverse = None
      match select_direction:
        case "top":
          reverse = True
        case "bottom":
          reverse = False
        case _:
          ValueError(f"'{select_direction}' is not a defined filter op")

      # create list of tuples (block, value)
      unsorted_blocks = zip(blocks, values)

      # sort blocks
      sorted_blocks = sorted(
        unsorted_blocks, key=lambda entry: entry[1], reverse=reverse
      )

      # truncate list if needed
      if select_limit < len(sorted_blocks):
        sorted_blocks = sorted_blocks[0:select_limit]

      # unzip list of (block, value) to just be a list of blocks
      sorted_blocks = list(map(lambda entry: entry[0], sorted_blocks))

      return allocate(["wteq", sorted_blocks], date, price_data, cache_data, fractional)
    case "group":
      # name = block[1]
      block = block[2]
      return allocate(block, date, price_data, cache_data, fractional)
    case "algo":
      # root node that when actually running is essentially the same as group
      # name = block[1]
      block = block[2]
      return allocate(block, date, price_data, cache_data, fractional)
    case _:
      raise ValueError(f"'{block_type}' is not a defined block")


def run_comparator(comparator, date, price_data, cache_data=None, fractional=None):
  op = comparator[0]

  # indicators
  lhs = run_indicator(comparator[1], date, price_data, cache_data, fractional)
  rhs = run_indicator(comparator[2], date, price_data, cache_data, fractional)

  match op:
    case "gt":
      return lhs > rhs
    case "gte":
      return lhs >= rhs
    case "lt":
      return lhs < rhs
    case "lte":
      return lhs <= rhs
    case _:
      raise ValueError(f"'{op}' is not a defined comparator")


def run_indicator(indicator, date, price_data, cache_data=None, fractional=None):
  op = indicator[0]
  block = indicator[1]

  match op:
    case "now":
      return now(block, date, price_data, cache_data, fractional, use_fractional_if_provided=False)
    case "cr":
      window_days = indicator[2]
      return run_cacheable_indicator(
        cr, block, date, window_days, price_data, cache_data, fractional, use_fractional_if_provided=False
      )
    case "ema":
      window_days = indicator[2]
      return run_cacheable_indicator(
        ema, block, date, window_days, price_data, cache_data, fractional, use_fractional_if_provided=False
      )
    case "ma":
      window_days = indicator[2]
      return run_cacheable_indicator(
        ma, block, date, window_days, price_data, cache_data, fractional, use_fractional_if_provided=False
      )
    case "mar":
      window_days = indicator[2]
      return run_cacheable_indicator(
        mar, block, date, window_days, price_data, cache_data, fractional, use_fractional_if_provided=False
      )
    case "mdd":
      window_days = indicator[2]
      return run_cacheable_indicator(
        mdd, block, date, window_days, price_data, cache_data, fractional, use_fractional_if_provided=False
      )
    case "rsi":
      window_days = indicator[2]
      return run_cacheable_indicator(
        rsi, block, date, window_days, price_data, cache_data, fractional, use_fractional_if_provided=False
      )
    case "stdev":
      window_days = indicator[2]
      return run_cacheable_indicator(
        stdev, block, date, window_days, price_data, cache_data, fractional, use_fractional_if_provided=False
      )
    case "stdevr":
      window_days = indicator[2]
      return run_cacheable_indicator(
        stdevr, block, date, window_days, price_data, cache_data, fractional, use_fractional_if_provided=False
      )
    case "number":
      return float(indicator[1])
    case _:
      raise ValueError(f"'{op}' is not a defined indicator")


def run_cacheable_indicator(
  indicator_fn, block, date, window_days, price_data, cache_data=None, fractional=None, use_fractional_if_provided=True
):
  cache_key = f"{indicator_fn.__name__}_{block}_{date}_{window_days}_{use_fractional_if_provided}"
  if cache_data is not None and cache_key in cache_data:
    return cache_data[cache_key]

  value = indicator_fn(block, date, window_days, price_data, cache_data, fractional, use_fractional_if_provided=use_fractional_if_provided)

  if cache_data is not None:
    cache_data[cache_key] = value

  return value


def now(block, date, price_data, cache_data=None, fractional=None, initial_value=None, use_fractional_if_provided=True):
  prices = price_history(block, date, 1, price_data, cache_data, fractional, initial_value, use_fractional_if_provided=use_fractional_if_provided)
  return prices[-1]


def cr(block, date, window_days, price_data, cache_data=None, fractional=None, initial_value=None, use_fractional_if_provided=True):
  offset = window_days + 1
  prices = price_history(block, date, offset, price_data, cache_data, fractional, initial_value, use_fractional_if_provided=use_fractional_if_provided)

  cr = (prices[-1] / prices[-offset]) - 1

  # convert to % to normalize
  #  how comparsons are made
  percent = cr * 100

  return percent


def ema(block, date, window_days, price_data, cache_data=None, fractional=None, initial_value=None, use_fractional_if_provided=True):
  # todo: I don't think I need to double the window days to get the right number
  num_days = window_days * 2
  prices = price_history(block, date, num_days, price_data, cache_data, fractional, initial_value, use_fractional_if_provided=use_fractional_if_provided)

  if num_days > len(prices):
    raise ValueError("Not enough data to calculate EMA")

  df = pd.DataFrame({"Close": prices})
  ema = ta.ema(df["Close"], length=window_days)
  value = ema[df.index[-1]]

  return value


def ma(block, date, window_days, price_data, cache_data=None, fractional=None, initial_value=None, use_fractional_if_provided=True):
  prices = price_history(block, date, window_days, price_data, cache_data, fractional, initial_value, use_fractional_if_provided=use_fractional_if_provided)

  # this isn't really "moving," but I get why we are calling it that
  ma = sum(prices) / float(len(prices))

  return ma


def mar(block, date, window_days, price_data, cache_data=None, fractional=None, initial_value=None, use_fractional_if_provided=True):
  prices = price_history(block, date, window_days + 1, price_data, cache_data, fractional, initial_value, use_fractional_if_provided=use_fractional_if_provided)

  df = pd.DataFrame({"Close": prices})
  ma = ta.sma(df["Close"].pct_change(), length=window_days)

  # convert to % to normalize how comparsons are made
  percent = ma[df.index[-1]] * 100

  return percent


def mdd(block, date, window_days, price_data, cache_data=None, fractional=None, initial_value=None, use_fractional_if_provided=True):
  prices = price_history(block, date, window_days, price_data, cache_data, fractional, initial_value, use_fractional_if_provided=use_fractional_if_provided)

  df = pd.DataFrame({"Close": prices})
  dd = ta.max_drawdown(df["Close"], method="percent")

  # convert to % to normalize how comparsons are made
  percent = dd * 100

  return percent


def rsi(block, date, window_days, price_data, cache_data=None, fractional=None, initial_value=None, use_fractional_if_provided=True):
  # "They use a 250 day lookback period (i.e. smoothing/warmup)" - @JasonKoz
  # https://discord.com/channels/1018958699991138386/1019589796802351106/1191042469262012416
  lookback_days = 250

  prices = price_history(
    block, date, window_days + lookback_days, price_data, cache_data, fractional, initial_value, use_fractional_if_provided=use_fractional_if_provided
  )

  # convert to DataFrame and run rsi method
  df = pd.DataFrame({"Close": prices})
  rsi = ta.rsi(df["Close"], length=window_days)[df.index[-1]]

  return rsi


def stdev(block, date, window_days, price_data, cache_data=None, fractional=None, initial_value=None, use_fractional_if_provided=True):
  prices = price_history(block, date, window_days, price_data, cache_data, fractional, initial_value, use_fractional_if_provided=use_fractional_if_provided)
  df = pd.DataFrame({"Close": prices})
  std = df["Close"].std()

  return std


def stdevr(block, date, window_days, price_data, cache_data=None, fractional=None, initial_value=None, use_fractional_if_provided=True):
  prices = price_history(block, date, window_days + 1, price_data, cache_data, fractional, initial_value, use_fractional_if_provided=use_fractional_if_provided)
  df = pd.DataFrame({"Close": prices})
  std = df["Close"].pct_change()[1:].std()

  # convert to % to normalize how comparsons are made
  percent = std * 100

  return percent

def backtest(initial_value, block, start_date, end_date, price_data, cache_data=None, fractional=None, use_fractional_if_provided=True):
  start_date = pd.to_datetime(start_date)
  end_date = pd.to_datetime(end_date)

  cache_key = f"backtest_{initial_value}_{block}_{start_date}_{end_date}"
  if cache_data is not None and cache_key in cache_data:
    return cache_data[cache_key]

  # use dates of trading data to find days
  range_start_index = price_data.index.get_loc(start_date)
  range_end_index = price_data.index.get_loc(end_date)
  td = price_data.iloc[range_start_index : range_end_index + 1]["Adj Close"]

  tickers = set()
  daily_allocations = {}
  for d in td.index:
    allocation = allocate(block, d, price_data, cache_data, fractional)
    tickers.update(allocation.keys())
    daily_allocations[str(d)] = allocation

  daily_portfolio = None

  values = []
  for d in td.index:
    allocations = daily_allocations[str(d)]

    portfolio_value = 0.0
    if daily_portfolio is None:
      if initial_value is not None:
        portfolio_value = initial_value
      else:
        for ticker, ticker_allocation in allocations.items():
          current_price = None
          if ticker == "$USD":
            current_price = 1
          else:
            current_price = td[ticker][d]

          portfolio_value += current_price
    else:
      for ticker, position in daily_portfolio.items():
        ticker_allocation, buy_price, shares_owned = position

        current_price = None
        if ticker == "$USD":
          current_price = 1
        else:
          current_price = td[ticker][d]

        portfolio_value += shares_owned * current_price

    daily_portfolio = {}
    invested_value = 0.0
    for ticker, ticker_allocation in allocations.items():
      current_price = td[ticker][d]
      cost_basis = portfolio_value * ticker_allocation
      shares_to_buy = None
      
      if fractional is None or not use_fractional_if_provided or fractional.get(ticker, True):
        shares_to_buy = cost_basis / current_price
      else:
        # franctional shares NOT allowed
        shares_to_buy = int(cost_basis / current_price)
        cost_basis = shares_to_buy * current_price
        ticker_allocation = cost_basis / portfolio_value

      invested_value += cost_basis

      daily_portfolio[ticker] = [ticker_allocation, current_price, shares_to_buy]

    uninvested_value = portfolio_value - invested_value
    daily_portfolio["$USD"] = [uninvested_value / portfolio_value, 1, uninvested_value]

    values.append((d, portfolio_value, daily_portfolio))

  if cache_data is not None:
    cache_data[cache_key] = values

  return values

def price_history(block, date, days, price_data, cache_data=None, fractional=None, initial_value=None, use_fractional_if_provided=True):
  date = pd.to_datetime(date)

  cache_key = f"price_history_{block}_{date}_{days}_{initial_value}"
  if cache_data is not None and cache_key in cache_data:
    return cache_data[cache_key]

  # use dates   of trading data to find days
  range_end_index = price_data.index.get_loc(date)
  range_start_index = max(0, range_end_index - (days - 1))

  simulation = backtest(initial_value, block, price_data.index[range_start_index],price_data.index[range_end_index], price_data, cache_data, fractional, use_fractional_if_provided=use_fractional_if_provided)

  values = []
  for d, portfolio_value, daily_portfolio in simulation:
    values.append(portfolio_value)

  if cache_data is not None:
    cache_data[cache_key] = values

  return values


def preprocess(fn, investable=False):
  algo_name = None
  algo_rebalance = None
  algo_threshold = None
  assets = set()
  investable_assets = set()
  indicators = []
  independent_blocks = []
  max_window_days = 0

  def merge(inner_fn, investable=False):
    nonlocal max_window_days

    summary = preprocess(inner_fn, investable=investable)
    assets.update(summary["assets"])
    investable_assets.update(summary["investable_assets"])
    # indicators.extend(summary["indicators"])
    independent_blocks.extend(summary["independent_blocks"])
    max_window_days = max(max_window_days, summary["max_window_days"])

  op = fn[0]
  args = fn[1:]
  match op:
    # blocks
    case "asset":
      ticker = args[0]
      assets.add(ticker)

      if investable:
        investable_assets.add(ticker)
    case "wteq" | "wtspec":
      blocks = args[0]

      for block in blocks:
        merge(block, investable=True)
    case "wtinvol":
      blocks = args[0]

      for block in blocks:
        merge(block, investable=True)
        independent_blocks.append(block)
    case "ifelse":
      comparator = args[0]
      true_block = args[1]
      false_block = args[2]

      merge(comparator, investable=False)
      merge(true_block, investable=True)
      merge(false_block, investable=True)
    case "filter":
      blocks = args[0]
      sort_indicator = args[1]
      # select = args[2]

      for block in blocks:
        merge(block, investable=True)
        independent_blocks.append(block)

      sort_op = sort_indicator[0]
      sort_window_days = sort_indicator[1]
      match sort_op:
        case "cr" | "mar" | "stdevr":
          sort_window_days = sort_window_days + 1
        case "rsi":
          # rsi has a "warm up" period
          # that needs to be accounted for
          sort_window_days = sort_window_days + 250

      max_window_days = max(max_window_days, sort_window_days)
    case "group":
      # name = args[0]
      block = args[1]

      merge(block, investable=True)
    case "algo":
      # algo values do not need to be merged. The assumption is that
      # there is only one algo block (if any) in an algo and it's the top
      # most value. This ensures that the algo name and rebalance values don't
      # get overwritten by an inner block
      algo_name = args[0]
      block = args[1]
      rebalance = args[2]

      if rebalance is not None:
        rebalance_type, rebalance_value = rebalance
        match rebalance_type:
          case "rebalance":
            if rebalance_value != "none" or rebalance_value != "none-set":
              algo_rebalance = rebalance_value
          case "threshold":
            algo_threshold = rebalance_value

      merge(block, investable=True)

    # comparators
    case "gt" | "gte" | "lt" | "lte":
      lhs_indicator = args[0]
      rhs_indicator = args[1]

      merge(lhs_indicator, investable=False)
      merge(rhs_indicator, investable=False)

    # indicators
    case "now":
      asset = args[0]
      merge(asset, investable=False)

      indicators.append(fn)
    case "cr" | "ema" | "ma" | "mar" | "mdd" | "rsi" | "stdev" | "stdevr":
      asset = args[0]
      window_days = args[1]
      merge(asset, investable=False)

      match op:
        case "cr" | "mar" | "stdevr":
          window_days = window_days + 1
        case "rsi":
          # rsi has a "warm up" period
          # that needs to be accounted for
          window_days = window_days + 250

      indicators.append(fn)

      max_window_days = max(max_window_days, window_days)
    case "number":
      # nothing to see here
      pass

    case _:
      raise ValueError(f"'{op}' is not a valid operation")

  return {
    "name": algo_name,
    "rebalance": algo_rebalance,
    "threshold": algo_threshold,
    "assets": assets,
    "investable_assets": investable_assets,
    # "indicators": indicators,
    "independent_blocks": independent_blocks,
    "max_window_days": max_window_days,
  }
