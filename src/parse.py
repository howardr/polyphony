def parse(node):
  match node["step"]:
    case "root":
      name = ""
      if "name" in node:
        name = node["name"]

      if "rebalance" in node:
        rebalance = ("rebalance", node["rebalance"])
      else:
        rebalance = ("rebalance", "none-set")

      # assumption that there can only be one child off of a root
      return ("algo", name, parse(node["children"][0]), rebalance)
    case "wt-cash-equal":
      return ("wteq", tuple(map(parse, node["children"])))
    case "wt-cash-specified":
      weights = tuple(
        map(
          lambda child: (float(child["weight"]["num"]), float(child["weight"]["den"])),
          node["children"],
        )
      )
      return ("wtspec", tuple(map(parse, node["children"])), weights)
    case "wt-inverse-vol":
      return ("wtinvol", tuple(map(parse, node["children"])), int(node["window-days"]))
    case "if":
      predicate_node = node["children"][0]
      true_node = predicate_node["children"][0]
      false_node = node["children"][1]["children"][0]
      return ("ifelse", predicate(predicate_node), parse(true_node), parse(false_node))
    case "asset":
      ticker = f"{node['ticker']}"
      return ("asset", ticker)
    case "filter":
      blocks = tuple(map(parse, node["children"]))

      sort_indicator = None
      if "sort-by-fn" in node:
        sort_indicator = filter_sort_indicator(node)

      select_fn = None
      if "select-fn" in node:
        select_fn = filter_select_fn(node)

      return ("filter", blocks, sort_indicator, select_fn)
    case "group":
      # todo : weight
      return ("group", node["name"], ("wteq", tuple(map(parse, node["children"]))))
    case _:
      raise ValueError(f"'{node['step']}' is not a defined step")


def predicate(node):
  comparator = node["comparator"]
  match comparator:
    case "gt" | "gte" | "lt" | "lte":
      indicator_lhs = indicator_fn("lhs", node)
      indicator_rhs = indicator_fn("rhs", node)

      return (comparator, indicator_lhs, indicator_rhs)
    case _:
      raise ValueError(f"'{comparator}' is not a defined predicate comparator")


def indicator_fn(side, node):
  if f"{side}-fixed-value?" in node and node[f"{side}-fixed-value?"]:
    return ("number", float(node[f"{side}-val"]))

  attr = node[f"{side}-fn"]
  match attr:
    case "current-price":
      return indicator_now(side, node)
    case "cumulative-return":
      return indicator_with_window_days("cr", side, node)
    case "exponential-moving-average-price":
      return indicator_with_window_days("ema", side, node)
    case "max-drawdown":
      return indicator_with_window_days("mdd", side, node)
    case "moving-average-price":
      return indicator_with_window_days("ma", side, node)
    case "moving-average-return":
      return indicator_with_window_days("mar", side, node)
    case "relative-strength-index":
      return indicator_with_window_days("rsi", side, node)
    case "standard-deviation-price":
      return indicator_with_window_days("stdev", side, node)
    case "standard-deviation-return":
      return indicator_with_window_days("stdevr", side, node)
    case _:
      raise ValueError(f"'{attr}' is not a defined {side}-fn")


def create_asset(ticker):
  return ("asset", ticker)


def indicator_now(side, node):
  ticker = node[f"{side}-val"]

  asset = create_asset(ticker)

  return ("now", asset)


def indicator_with_window_days(op, side, node):
  ticker = node[f"{side}-val"]
  days = None

  if f"{side}-window-days" in node:
    days = node[f"{side}-window-days"]
  elif f"{side}-fn-params" in node:
    days = node[f"{side}-fn-params"]["window"]

  asset = create_asset(ticker)

  return (op, asset, int(days))


def filter_select_fn(node):
  return (node["select-fn"], int(node["select-n"]))


def filter_sort_indicator(node):
  attr = node["sort-by-fn"]

  days = None

  if "sort-by-window-days" in node:
    days = node["sort-by-window-days"]
  elif "sort-by-fn-params" in node:
    days = node["sort-by-fn-params"]["window"]
  else:
    raise ValueError(f"'window' is not defined for {attr} filter sort")

  days = int(days)

  match attr:
    case "cumulative-return":
      return ("cr", days)
    case "exponential-moving-average-price":
      return ("ema", days)
    case "max-drawdown":
      return ("mdd", days)
    case "moving-average-price":
      return ("ma", days)
    case "moving-average-return":
      return ("mar", days)
    case "relative-strength-index":
      return ("rsi", days)
    case "standard-deviation-price":
      return ("stdev", days)
    case "standard-deviation-return":
      return ("stdevr", days)
    case _:
      raise ValueError(f"'{attr}' is not a defined sort-fn")
