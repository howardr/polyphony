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

def pi(str, indent=0, prefix="", is_first_line=False):
  if is_first_line:
    print(f"{indent * ' '}{prefix}{str}")
  else:
    print(f"{(indent + len(prefix)) * ' '}{str}")

def comparator_str(comparator):
  op = comparator[0]
  args = comparator[1:]

  lhs_indicator = args[0]
  rhs_indicator = args[1]

  op_str = None
  match op:
    case "gt":
      op_str = ">"
    case "gte":
      op_str = ">="
    case "lt":
      op_str = "<"
    case "lte":
      op_str = "<="

  return f"{indicator_str(lhs_indicator)} {op_str} {indicator_str(rhs_indicator)}"
  
def indicator_str(indicator):
  op = indicator[0]
  args = indicator[1:]

  str = None
  match op:
    case "cr" | "ema" | "ma" | "mar" | "mdd" | "rsi" | "stdev" | "stdevr":
      asset = args[0]
      window_days = args[1]
      str = f"{op}({asset_str(asset[1])}, {window_days} days)"
    case "now":
      asset = args[0]
      str = f"{op}({asset_str(asset[1])})"
    case "number":
      str = f"{args[0]}"
    case _:
      raise ValueError(f"'{op}' is not a valid operation")

  return str

def asset_str(asset_name):
  return f"${asset_name}"

def pp(fn, indent=0, first_line_prefix=""):
  op = fn[0]
  args = fn[1:]

  match op:
    case "wteq":
      blocks = args[0]
      if len(blocks) == 1:
        # this prevents a bunch of nested wteq with one block
        pp(blocks[0], indent)
      else:
        pi(op, indent, prefix=first_line_prefix, is_first_line=True)
        for b in blocks:
          pp(b, indent, first_line_prefix="- ")
    case "ifelse":
      comparator = args[0]
      true_block = args[1]
      false_block = args[2]

      pi(f"if {comparator_str(comparator)}", indent, prefix=first_line_prefix, is_first_line=True)
      pp(true_block, indent + 2)
      pi("else", indent)
      pp(false_block, indent + 2)
    case "asset":
      asset_name = args[0]
      pi(asset_str(asset_name), indent, prefix=first_line_prefix, is_first_line=True)
    case "filter":
      blocks = args[0]
      sort_indicator = args[1]
      select = args[2]

      sort_str = None
      match sort_indicator[0]:
        case "cr" | "ema" | "ma" | "mar" | "mdd" | "rsi" | "stdev" | "stdevr":
          sort_str = f"{sort_indicator[0]}({sort_indicator[1]} days)"
        case _:
          raise ValueError(f"'{sort_indicator[0]}' is not a valid sort indicator")

      pi(f"select {select[0]} {select[1]} sort by {sort_str}", indent, prefix=first_line_prefix, is_first_line=True)
      for b in blocks:
        pp(b, indent, first_line_prefix="- ")
    case _:
      print(fn)
      exit()

print(algo)

print("===")

pp(algo)
