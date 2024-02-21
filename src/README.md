
## Allocations

### _Allocation_

A map of tickers and percentages (in decimals). The sum of percentages will always add up to `1`.

```python
{
  'SPY': 0.5
  'XLE': 0.5
}
```

Generate an _Allocation_

```python
import datetime
import yfinance as yf

# define an algo
algo = ['wteq', [
  ['asset', 'SPY'],
  ['asset', 'XLE']
]]

allocation = allocate(algo, date, trading_data)
```

#### `allocate`
#### `preprocess`

## Algo

An `Algo` is a serialized simple representation of a daily trading algorithm.

Simple Example

```python
# Equal allocation between SPY, QQQ, and XLE
["wteq", [
  ["asset", "SPY"],
  ["asset", "QQQ"],
  ["asset", "XLE"]
]]
```

More Complex

```python
# My Algo
# if the current price of SPY > 200d moving average of SPY then
#     allocate quality between SPY, QQQ, XLE
# otherwise
#     invest only in BIL
["group", "My Algo", [
["ifelse", 
  ["gt", ["now", "SPY"], ["ma", "SPY", 200]],
  ["wteq", [
    ["asset", "SPY"],
    ["asset", "QQQ"],
    ["asset", "XLE"]
  ]],
  ["asset", "BIL"]
]
]]
```

### Primitive Objects

* _String_ `"foo"` or `'bar'`
* _Number_ `1`, `2.3`, or `-0.4`
* _Boolean_ `true` or `false`
* _List_ `[]` or `["one", 2, false]`

### Predicate Object

A _Predicate_ is a _List_ where the first entry is a name (_String_) and at least one additional _Object_ which arg called arguments or args. A _Predicate_ always returns an _Object_.

```
['op', 'arg1', 'arg2'] -> Predicate
```

Using a specific example

```
['asset', 'SPY'] -> Block
```

### Core Predicates

* _Block_
* _Indicator_
* _Comparator_

#### Block ####

A _Block_ is an abstract allocatable collection of one or more assets.

There are a few types: `asset`, `ifelse`, `wteq`, `filter`, `group`

##### `asset`

```
['asset', String ticker]
```

Examples

```python
# Example 1
['asset', 'SPY']

# Example 2
['asset', 'QQQ']

# Example 3
['asset', 'XLE']
```

##### `wteq`

```
['wteq', Block[] blocks]
```

Examples

```python
# Example 1
['wteq', [
  ['asset', 'SPY'],
  ['asset', 'QQQ'],
  ['asset', 'XLE']
]]

# Example 2
['wteq', [
  ['asset', 'SPY'],
  ['wteq', [
    ['asset', 'QQQ'],
    ['asset', 'XLE']
  ]]
]]

# Example 3
['wteq', [
  ['asset', 'SPY'],
  ['ifelse',
    ['gt', ['rsi', 'SPY', 15], ['number', 80]],
    ['asset', 'BIL'],
    ['asset', 'TQQQ']
  ]
]]
```

##### `ifelse`

```
['ifelse', Conditional conditional, Block true_block, Block false_block]
```

Examples

```python
# Example 1
['ifelse',
  ['gt', ['now', 'SPY'], ['ma', 'SPY', 200]],
  ['asset', 'BIL'],
  ['asset', 'TQQQ']
]

# Example 1 (annotated)
['ifelse',
  # conditional
  # current price of SPY > 200d average of SPY
  ['gt', ['now', 'SPY'], ['ma', 'SPY', 200]],

  # true_block
  # if conditional true, use BIL
  ['asset', 'BIL'],

  # false_block
  # if conditional false, use TQQQ
  ['asset', 'TQQQ']
]
```

##### `filter`

```
['filter', Block[] blocks, FilterIndicator indicator, FilterSelect select]
```

Examples

```python
# Example 1
['filter',
  [
    ['asset', 'SPY'],
    ['asset', 'QQQ'],
    ['asset', 'XLE']
  ],
  ['cr', 10],
  ['top', 1]
]

# Example 1 (annotated)
['filter',
  # list of Blocks
  [
    ['asset', 'SPY'],
    ['asset', 'QQQ'],
    ['asset', 'XLE']
  ],

  # filter sort
  # sort blocks by 10 day cumulative return
  ['cr', 10],

  # filter select
  # select top 1 of sorted blocks
  ['top', 1]
]
```

##### `group`

```
['group', String name, Block block]
```

Examples

```python
# Example 1
['group', 'My Algo', 
  ['wteq', [
    ['asset', 'SPY'],
    ['asset', 'QQQ'],
    ['asset', 'XLE']
  ]]
]
```

#### Indicator ####

An _Indicator_ runs a calculation on an asset and returns a _Number_.

There are a few types: `now`, `car`, `ma`, `mar`, `number`, `rsi`

##### `now` - Current Price

```
['now', String ticker]
```

Examples

```python
# Example 1
['now', 'SPY']
```

##### `cr` - Cumulative Return

```
['cr', String ticker, Number window_days]
```

Examples

```python
# Example 1
# 10d cumulative return of SPY
['cr', 'SPY', 10]
```

##### `ma` - Moving Average

```
['ma', String ticker, Number window_days]
```

Examples

```python
# Example 1
# 10d moving average of SPY
['ma', 'SPY', 10]
```

##### `mar` - Moving Average Return

```
['mar', String ticker, Number window_days]
```

Examples

```python
# Example 1
# 10d moving average return of SPY
['mar', 'SPY', 10]
```

##### `Number` - Number

Used in a _Comparator_ as a fixed value.

```
['number', Number number]
```

Examples

```python
# Example 1
# 10d moving average return of SPY
['number', 99.5]

# Example 2 (annotated)
['ifelse'.
  # lt (or <) only accepts an Indicator as arguments
  # `number` is used in cases when a comparison is made against a fixed number
  ['lt',
    # 10 day RSI of SPY < 90
    ['rsi', 'SPY', 10],
    ['number', 90]
  ],
  ['asset', 'SPY'],
  ['asset', 'BIL']
]
```

##### `rsi` - Relative Strength Index

```
['rsi', String ticker, Number window_days]
```

Examples

```python
# Example 1
# 10d relative strength index of SPY
['rsi', 'SPY', 10]
```

#### Comparator ####

A _Comparator_ compares two _Indicators_ and returns a _Boolean_.

There are a few types: `gt`, `gte`, `lt`, `lte`

##### `gt` - _>_ Greater Than

```
['gt', Indicator lhs, Indicator rhs]
```

Examples

```python
# Example 1
['gt',
  ['ma', 'SPY', 10],
  ['ma', 'SPY', 60],
]

# Example 1 (annotated)
# 10d moving average of SPY > 60d moving average of SPY
['gt',

  # lhs (left hand side)
  # 10d moving average of SPY
  ['ma', 'SPY', 10],

  # rhs (right hand side)
  # 60d moving average of SPY
  ['ma', 'SPY', 60]
]
```

##### `gte` - _>=_ Greater Than or Equal To

```
['gte', Indicator lhs, Indicator rhs]
```

Examples

```python
# Example 1
['gte',
  ['ma', 'SPY', 10],
  ['ma', 'SPY', 60],
]

# Example 1 (annotated)
# 10d moving average of SPY >= 60d moving average of SPY
['gte',

  # lhs (left hand side)
  # 10d moving average of SPY
  ['ma', 'SPY', 10],

  # rhs (right hand side)
  # 60d moving average of SPY
  ['ma', 'SPY', 60]
]
```

##### `lt` - _<_ Less Than

```
['lt', Indicator lhs, Indicator rhs]
```

Examples

```python
# Example 1
['lt',
  ['ma', 'SPY', 10],
  ['ma', 'SPY', 60],
]

# Example 1 (annotated)
# 10d moving average of SPY < 60d moving average of SPY
['lt',

  # lhs (left hand side)
  # 10d moving average of SPY
  ['ma', 'SPY', 10],

  # rhs (right hand side)
  # 60d moving average of SPY
  ['ma', 'SPY', 60]
]
```

##### `lte` - _<=_ Les Than or Equal To

```
['lte', Indicator lhs, Indicator rhs]
```

Examples

```python
# Example 1
['lte',
  ['ma', 'SPY', 10],
  ['ma', 'SPY', 60],
]

# Example 1 (annotated)
# 10d moving average of SPY <= 60d moving average of SPY
['lte',

  # lhs (left hand side)
  # 10d moving average of SPY
  ['ma', 'SPY', 10],

  # rhs (right hand side)
  # 60d moving average of SPY
  ['ma', 'SPY', 60]
]
```