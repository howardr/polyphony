import datetime
import random
import pandas as pd
import pandas_ta as ta
import pytest
from allocate import allocate, preprocess, run_indicator

WINDOW_INDICATOR_TYPES = ["cr", "ema", "ma", "mar", "mdd", "rsi", "stdev", "stdevr"]
ALL_INDICATOR_TYPES = ["now"] + WINDOW_INDICATOR_TYPES

def test_allocate():
  assert True

def test_allocate_asset():
  date = datetime.date(2024, 2, 6)
  stock_data = None

  expected = {'asset1': 1.0}

  result = allocate(('asset', 'asset1'), date, stock_data)

  assert result == expected

def test_allocate_wteq_assets():
  date = datetime.date(2024, 2, 6)
  stock_data = None

  expected = {
    'asset1': 0.5,
    'asset2': 0.5,
  }

  result = allocate(('wteq', (
    ('asset', 'asset1'),
    ('asset', 'asset2')
  )), date, stock_data)

  assert result == expected

def test_allocate_wtspec_assets():
  date = datetime.date(2024, 2, 6)
  stock_data = None

  expected = {
    'asset1': 0.9,
    'asset2': 0.1,
  }

  result = allocate(('wtspec', (
    ('asset', 'asset1'),
    ('asset', 'asset2')
  ), (
    (90, 100),
    (10, 100)
  )), date, stock_data)

  assert result == expected

def test_allocate_wtinvol_assets():
  date = pd.to_datetime('2023-01-06')

  price_data = pd.DataFrame({
    ('Adj Close', 'asset1'): [100, 110, 132],
    ('Adj Close', 'asset2'): [100, 90, 85.5]
  }, index=pd.date_range('2023-01-04', periods=3))
  price_data.columns.names = ['Price', 'Ticker']

  expected = {
    'asset1': 5 / 15,
    'asset2': 10 / 15,
  }

  result = allocate(('wtinvol', (
    ('asset', 'asset1'),
    ('asset', 'asset2')
  ), 2), date, price_data)

  assert result == expected

def test_allocate_ifelse_true_assets():
  date = datetime.date(2024, 2, 6)
  stock_data = None

  expected = {
    'asset1': 1,
  }

  result = allocate(('ifelse',
    ('gt', ['number', 1], ['number', 0]),
    ('asset', 'asset1'),
    ('asset', 'asset2')
  ), date, stock_data)

  assert result == expected

def test_allocate_ifelse_false_assets():
  date = datetime.date(2024, 2, 6)
  stock_data = None

  expected = {
    'asset2': 1,
  }

  result = allocate(('ifelse',
    ('gt', ['number', 0], ['number', 1]),
    ('asset', 'asset1'),
    ('asset', 'asset2')
  ), date, stock_data)

  assert result == expected


def test_allocate_group_assets():
  date = datetime.date(2024, 2, 6)
  stock_data = None

  expected = {
    'asset1': 0.5,
    'asset2': 0.5,
  }

  result = allocate(('group', 'My Group', ('wteq', (
    ('asset', 'asset1'),
    ('asset', 'asset2')
  ))), date, stock_data)

  assert result == expected

def test_allocate_indicator_now():
  date = pd.to_datetime('2023-01-06')
  price_data = pd.DataFrame({
    ('Adj Close', 'asset1'): [100, 105, 110, 115, 120, 125],
  }, index=pd.date_range('2023-01-01', periods=6))
  price_data.columns.names = ['Price', 'Ticker']

  indicator = ('now', ('asset', 'asset1'))
  value = run_indicator(indicator, date, price_data)

  assert value == 125


def test_allocate_indicator_cr():
  date = pd.to_datetime('2023-01-06')
  price_data = pd.DataFrame({
    ('Adj Close', 'CONL'): [100, 105, 110, 115, 120, 125],
  }, index=pd.date_range('2023-01-01', periods=6))
  price_data.columns.names = ['Price', 'Ticker']

  lhs_indicator = ('cr', ('asset', 'CONL'), 1)
  lhs = run_indicator(lhs_indicator, date, price_data)

  rhs_indicator = ('cr', ('asset', 'CONL'), 5)
  rhs = run_indicator(rhs_indicator, date, price_data)

  assert lhs == ((125 / 120) -1) * 100
  assert rhs == ((125 / 100) -1) * 100
  assert lhs < rhs

  summary = preprocess(lhs_indicator)
  assert summary["max_window_days"] == 2

  summary = preprocess(rhs_indicator)
  assert summary["max_window_days"] == 6


def test_allocate_indicator_ema():
  date = pd.to_datetime('2023-01-06')
  price_data = pd.DataFrame({
    ('Adj Close', 'SPY'): [100, 105, 110, 115, 120, 125],
  }, index=pd.date_range('2023-01-01', periods=6))
  price_data.columns.names = ['Price', 'Ticker']

  indicator = ('ema', ('asset', 'SPY'), 3)
  ema = run_indicator(indicator, date, price_data)

  df = pd.DataFrame({"Close": [115, 120, 125]})
  expected = ta.ema(df["Close"], length=3)

  assert ema == expected[df.index[-1]]

  summary = preprocess(indicator)
  assert summary["max_window_days"] == 3


def test_allocate_indicator_ma():
  date = pd.to_datetime('2023-01-05')
  price_data = pd.DataFrame({
    ('Adj Close', 'SPY'): [100, 105, 110, 115, 120, 125],
  }, index=pd.date_range('2023-01-01', periods=6))
  price_data.columns.names = ['Price', 'Ticker']

  indicator = ('ma', ('asset', 'SPY'), 2)
  ma = run_indicator(indicator, date, price_data)

  expected = (115 + 120) / 2

  assert ma == expected

  summary = preprocess(indicator)
  assert summary["max_window_days"] == 2

def test_allocate_indicator_mar():
  date = pd.to_datetime('2023-01-06')
  price_data = pd.DataFrame({
    ('Adj Close', 'SPY'): [100, 105, 110, 115, 120, 125],
  }, index=pd.date_range('2023-01-01', periods=6))
  price_data.columns.names = ['Price', 'Ticker']

  indicator = ('mar', ('asset', 'SPY'), 2)
  mar = run_indicator(indicator, date, price_data)

  pct_returns = [
    (120.0 / 115.0) - 1.0,
    (125.0 / 120.0) - 1.0
  ]
  expected = (sum(pct_returns) / len(pct_returns)) * 100

  assert mar == expected

  summary = preprocess(indicator)
  assert summary["max_window_days"] == 3

def test_allocate_indicator_mdd():
  date = pd.to_datetime('2023-01-09')

  prices = [100, 105, 90, 95, 80, 110, 90, 120, 125]

  price_data = pd.DataFrame({
    ('Adj Close', 'SPY'): prices,
  }, index=pd.date_range('2023-01-01', periods=9))
  price_data.columns.names = ['Price', 'Ticker']

  indicator = ('mdd', ('asset', 'SPY'), 9)
  mdd = run_indicator(indicator, date, price_data)

  expected = ((105 - 80) / 105) * 100

  # rounding bc they seem to be off by a tiny bit
  assert round(mdd, 3) == round(expected, 3)

  summary = preprocess(indicator)
  assert summary["max_window_days"] == 9


def test_allocate_indicator_rsi():
  window_days = 6
  lookback = 250
  periods = window_days + lookback
  prices = [random.uniform(90.0, 150.0) for _ in range(periods)]

  price_data = pd.DataFrame({
    ('Adj Close', 'SPY'): prices,
  }, index=pd.date_range('2023-01-01', periods=periods))
  price_data.columns.names = ['Price', 'Ticker']

  end_date = price_data.index[-1]

  indicator = ('rsi', ('asset', 'SPY'), window_days)
  rsi = run_indicator(indicator, end_date, price_data)

  df = pd.DataFrame({"Close": prices})
  expected = ta.rsi(df["Close"], length=window_days)[df.index[-1]]

  assert rsi == expected

  summary = preprocess(indicator)
  assert summary["max_window_days"] == periods


def test_allocate_indicator_stdev():
  date = pd.to_datetime('2023-01-06')

  prices = [95, 80, 110, 90, 120, 125]

  price_data = pd.DataFrame({
    ('Adj Close', 'SPY'): prices,
  }, index=pd.date_range('2023-01-01', periods=6))
  price_data.columns.names = ['Price', 'Ticker']

  indicator = ('stdev', ('asset', 'SPY'), 6)
  std = run_indicator(indicator, date, price_data)

  df = pd.DataFrame({"Close": prices})
  expected = df["Close"].std()

  assert std == expected

  summary = preprocess(indicator)
  assert summary["max_window_days"] == 6


def test_allocate_indicator_stdevr():
  date = pd.to_datetime('2023-01-08')
  window_days = 6

  prices = [200, 100, 95, 80, 110, 90, 120, 125]

  price_data = pd.DataFrame({
    ('Adj Close', 'SPY'): prices,
  }, index=pd.date_range('2023-01-01', periods=8))
  price_data.columns.names = ['Price', 'Ticker']

  indicator = ('stdevr', ('asset', 'SPY'), window_days)
  std = run_indicator(indicator, date, price_data)

  df = pd.DataFrame({"Close": prices})
  expected = df["Close"].pct_change()[-window_days:].std() * 100

  assert std == expected

  summary = preprocess(indicator)
  assert summary["max_window_days"] == (window_days + 1)


def test_allocate_indicator_caching_correct_values():
  date = pd.to_datetime('2023-01-06')
  price_data = pd.DataFrame({
    ('Adj Close', 'SPY'): [100, 105, 110, 115, 120, 125],
  }, index=pd.date_range('2023-01-01', periods=6))
  price_data.columns.names = ['Price', 'Ticker']

  for indicator_type in WINDOW_INDICATOR_TYPES:
    indicator = (indicator_type, ('asset', 'SPY'), 3)
    cache_data = {}
    uncached = run_indicator(indicator, date, price_data, cache_data)
    cached = run_indicator(indicator, date, price_data, cache_data)

    assert uncached == cached

def test_allocate_coerce_datetime():
  date = datetime.date(2023, 1, 6)
  price_data = pd.DataFrame({
    ('Adj Close', 'SPY'): [100, 105, 110, 115, 120, 125],
  }, index=pd.date_range('2023-01-01', periods=6))
  price_data.columns.names = ['Price', 'Ticker']

  expected = {
    'SPY': 1.0
  }

  for indicator_type in WINDOW_INDICATOR_TYPES:
    actual = allocate(('ifelse',
      ('gt', (indicator_type, ['asset', 'SPY'], 3), ['number', -100.0]), # using -100 to make sure this alwasy evaluates as true
      ['asset', 'SPY'],
      ['asset', 'BIL']
    ), date, price_data)

    assert actual == expected

def test_allocate_filter_top_assets():
  date = datetime.date(2023, 1, 2)
  window_days = 1

  # todo: figure out what happens if there is a "tie" in a sort
  price_data = pd.DataFrame({
    ('Adj Close', 'asset1'): [80, 75],
    ('Adj Close', 'asset2'): [120, 125],
    ('Adj Close', 'asset3'): [140, 200],
  }, index=pd.date_range('2023-01-01', periods=2))
  price_data.columns.names = ['Price', 'Ticker']

  expected_allocation_by_indicator = {
    "mdd": {
      "asset1": 0.5,
      "asset2": 0.5,
    },
    "stdev": {
      "asset1": 0.5,
      "asset2": 0.5,
    },
    "stdevr": {
      "asset1": 0.5,
      "asset2": 0.5,
    },
    "default": {
      "asset2": 0.5,
      "asset3": 0.5,
    }
  }

  expected_max_window_days = {
    "cr": window_days + 1,
    "mar": window_days + 1,
    "stdevr": window_days + 1,
    "rsi": window_days + 250,
    "default": 1,
  }

  for indicator_type in WINDOW_INDICATOR_TYPES:
    algo = ('filter',
      (
        ('asset', 'asset1'),
        ('asset', 'asset2'),
        ('asset', 'asset3'),
      ),
      (indicator_type, window_days),
      ('top', 2)
    )

    result = allocate(algo, date, price_data)

    expected = None
    if indicator_type in expected_allocation_by_indicator:
      expected = expected_allocation_by_indicator[indicator_type]
    else:
      expected = expected_allocation_by_indicator["default"]

    assert result == expected, f"Incorrect allocation for indicator type: {indicator_type}"

    summary = preprocess(algo)
    expected_period = None
    if indicator_type in expected_max_window_days:
      expected_period = expected_max_window_days[indicator_type]
    else:
      expected_period = expected_max_window_days["default"]
    assert summary["max_window_days"] == expected_period, f"Incorrect max window days for indicator type: {indicator_type}"