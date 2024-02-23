import datetime
import pandas as pd
import pandas_ta as ta
import pytest
from unittest.mock import MagicMock, Mock, patch
from allocate import allocate, run_indicator

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

def test_allocate_indicator_caching_correct_values():
  date = pd.to_datetime('2023-01-06')
  price_data = pd.DataFrame({
    ('Adj Close', 'SPY'): [100, 105, 110, 115, 120, 125],
  }, index=pd.date_range('2023-01-01', periods=6))
  price_data.columns.names = ['Price', 'Ticker']

  ops = ["cr", "ema", "ma", "mar", "mdd", "rsi", "stdev", "stdevr"]
  for op in ops:
    indicator = (op, ('asset', 'SPY'), 3)
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

  ops = ["cr", "ema", "ma", "mar", "mdd", "rsi", "stdev", "stdevr"]
  for op in ops:
    actual = allocate(('ifelse',
      ('gt', (op, ['asset', 'SPY'], 3), ['number', -100.0]), # using -100 to make sure this alwasy evaluates as true
      ['asset', 'SPY'],
      ['asset', 'BIL']
    ), date, price_data)

    assert actual == expected

def test_allocate_filter_top_assets():
  date = datetime.date(2023, 1, 2)

  # todo: figure out what happens if there is a "tie" in a sort
  price_data = pd.DataFrame({
    ('Adj Close', 'asset1'): [80, 75],
    ('Adj Close', 'asset2'): [120, 125],
    ('Adj Close', 'asset3'): [140, 200],
  }, index=pd.date_range('2023-01-01', periods=2))
  price_data.columns.names = ['Price', 'Ticker']

  expected = {
    'asset2': 0.5,
    'asset3': 0.5,
  }

  result = allocate(('filter',
    (
      ('asset', 'asset1'),
      ('asset', 'asset2'),
      ('asset', 'asset3'),
    ),
    ('cr', 1),
    ('top', 2)
  ), date, price_data)

  assert result == expected