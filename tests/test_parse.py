import pytest
from parse import parse

def test_parse_symph_tqqq_ftlt():
  #hwrdr - TQQQ For The Long Term (Reddit Post Link)
  #https://backtest-api.composer.trade/api/v1/public/symphonies/wmDK13UrFbWbObhmnQLG/score
  # blocks: wteq, ifelse, filter, asset
  # indicators: now, ma, rsi, number
  # sorts: ma, rsi
  # comparators: lt, gt,
  # select: top, bottom
  symphony_json = {"id":"wmDK13UrFbWbObhmnQLG","step":"root","name":"hwrdr - TQQQ For The Long Term (Reddit Post Link)","description":"","rebalance":"daily","children":[{"id":"55d4cd1f-e631-48f9-9ec0-fa9d66e4ccee","step":"wt-cash-equal","children":[{"id":"5a12f26b-f2c9-4a88-8bb3-067557426e5e","step":"wt-cash-equal","children":[{"weight":{"num":100,"den":100},"id":"9a471655-8344-40b1-a26c-4d2267c73758","step":"if","children":[{"children":[{"id":"9ab6e988-d8df-48a8-b8e2-558c7525bffc","step":"wt-cash-equal","children":[{"id":"83ac7f18-f51b-4f0c-81fe-a13af8b8e399","step":"if","children":[{"children":[{"ticker":"VIXY","exchange":"BATS","name":"ProShares VIX Short-Term Futures ETF","id":"25928b5e-4d61-4650-a0f9-390bf7c73917","step":"asset","children-count":0}],"is-else-condition?":False,"rhs-fixed-value?":True,"lhs-fn":"relative-strength-index","lhs-window-days":"10","lhs-val":"TQQQ","id":"50d39ec5-0d69-4b0a-b637-36d51dd61b39","comparator":"gt","rhs-val":"79","step":"if-child","collapsed?":False},{"id":"70c7eadb-4b31-460f-907b-71e31da2c743","step":"if-child","is-else-condition?":True,"children":[{"id":"965ede5c-c51c-4f55-ab5e-afac5b48bc9e","step":"wt-cash-equal","children":[{"id":"f71d63f0-ce6b-4265-b880-f059d2a5b981","step":"if","children":[{"children":[{"ticker":"VIXY","exchange":"BATS","name":"ProShares VIX Short-Term Futures ETF","id":"c75e8db3-2de1-430a-986c-c2673276c246","step":"asset","children-count":0}],"is-else-condition?":False,"rhs-fixed-value?":True,"lhs-fn":"relative-strength-index","lhs-window-days":"10","lhs-val":"SPXL","id":"d5195b59-4a4f-43f3-8de4-e1d4a6c1da29","comparator":"gt","rhs-val":"80","step":"if-child"},{"id":"805cbb4e-2952-4c3a-bc81-1d01481bee23","step":"if-child","is-else-condition?":True,"children":[{"id":"7a62b727-a046-4535-ac8e-d48371d2db3c","step":"wt-cash-equal","children":[{"name":"ProShares UltraPro QQQ","ticker":"TQQQ","has_marketcap":False,"id":"c0145c27-f597-4caa-8c03-d2c417bdc8e9","exchange":"XNAS","price":18.92,"step":"asset","dollar_volume":5.535417683400001E9}]}]}]}],"collapsed?":False}]}]}]}],"rhs-fn":"moving-average-price","is-else-condition?":False,"lhs-fn":"current-price","rhs-window-days":"200","lhs-val":"SPY","id":"2c6de17e-d41b-41b4-b458-7a734b817c0a","comparator":"gt","rhs-val":"SPY","step":"if-child","collapsed?":False},{"id":"fbe0943b-8ac2-4100-ab0e-e3bbed88118e","step":"if-child","is-else-condition?":True,"children":[{"id":"46362f5a-a635-4b8a-90cb-4121419f62b3","step":"wt-cash-equal","children":[{"id":"988d50db-dd89-4cde-bfb3-b5d4553a29bf","step":"if","children":[{"children":[{"name":"Direxion Daily Technology Bull 3x Shares","ticker":"TECL","has_marketcap":False,"id":"d8a55927-4216-46d3-a079-99d86afbc0ab","exchange":"ARCX","price":23.24,"step":"asset","dollar_volume":1.293694108E8}],"is-else-condition?":False,"rhs-fixed-value?":True,"lhs-fn":"relative-strength-index","lhs-window-days":"10","lhs-val":"TQQQ","id":"504f7192-56a7-4470-aee6-728862893239","comparator":"lt","rhs-val":"31","step":"if-child","collapsed?":False},{"id":"9656f3e7-a985-49d9-b892-8c87e268d09a","step":"if-child","is-else-condition?":True,"children":[{"id":"05e69978-544d-40a6-a6cd-ecebb93eeb56","step":"wt-cash-equal","children":[{"id":"022d6bcf-28c4-42bd-a3fc-26b27b7af070","step":"if","children":[{"children":[{"name":"ProShares UltraPro S&P500","ticker":"UPRO","has_marketcap":False,"id":"c2582e3d-56d7-4a14-ba9c-70f998552301","exchange":"ARCX","price":28.41,"step":"asset","dollar_volume":5.2527686514E8}],"is-else-condition?":False,"rhs-fixed-value?":True,"lhs-fn":"relative-strength-index","lhs-window-days":"10","lhs-val":"SPY","id":"4c87e5ce-9795-4540-a2c3-0a915a8e6932","comparator":"lt","rhs-val":"30","step":"if-child","collapsed?":False},{"id":"30644bcf-e126-4449-9a80-b27b18983aea","step":"if-child","is-else-condition?":True,"children":[{"id":"af77345e-331b-4c3e-875c-516b4d81d7c7","step":"wt-cash-equal","children":[{"id":"bcc2169b-136e-4a86-b119-35bca8dc7d40","step":"if","children":[{"children":[{"id":"74c0023a-a50e-4edd-b0fa-167ad27a64ed","step":"wt-cash-equal","children":[{"select?":True,"children":[{"name":"ProShares UltraPro Short QQQ","ticker":"SQQQ","has_marketcap":False,"id":"2982fba0-5713-45be-9b7a-43fd69133a6c","exchange":"XNAS","price":61.32,"step":"asset","dollar_volume":9.65597774064E9},{"name":"iShares 20+ Year Treasury Bond ETF","ticker":"TLT","has_marketcap":False,"id":"f1d68991-9911-40ff-a217-d56ffcf2de97","exchange":"XNAS","price":105.7,"step":"asset","dollar_volume":1.3700322412E9,"children-count":0}],"select-fn":"top","select-n":"1","sort-by-fn":"relative-strength-index","sort-by-window-days":"10","id":"c89738ea-0bae-4fbb-94f1-aef5048fe10b","sort-by?":True,"step":"filter"}]}],"rhs-fn":"moving-average-price","is-else-condition?":False,"lhs-fn":"current-price","rhs-window-days":"20","lhs-val":"TQQQ","id":"b5ce2d31-5cf6-47f8-87de-f7bfb12f391d","comparator":"lt","rhs-val":"TQQQ","step":"if-child","collapsed?":False},{"id":"d0326c58-73d6-49c1-8162-7590cc5544bd","step":"if-child","is-else-condition?":True,"children":[{"id":"fce80c8a-8bdc-4afc-a547-dbb077ad2ad9","step":"wt-cash-equal","children":[{"id":"c010620b-9806-487e-8e36-b4cd8fa61671","step":"if","children":[{"children":[{"name":"ProShares UltraPro Short QQQ","ticker":"SQQQ","has_marketcap":False,"id":"9f7a293e-5a17-43f7-921d-6040e5933ab7","exchange":"XNAS","price":61.32,"step":"asset","dollar_volume":9.65597774064E9}],"is-else-condition?":False,"rhs-fixed-value?":True,"lhs-fn":"relative-strength-index","lhs-window-days":"10","lhs-val":"SQQQ","id":"87865f18-5bce-4e05-bb3c-bec089cd27da","comparator":"lt","rhs-val":"31","step":"if-child"},{"id":"ec8b8901-9652-407f-85a7-d82f1d01a311","step":"if-child","is-else-condition?":True,"children":[{"name":"ProShares UltraPro QQQ","ticker":"TQQQ","has_marketcap":False,"id":"cffede64-5415-44d4-a9b2-9c98d1ac8af4","exchange":"XNAS","price":21.73,"step":"asset","dollar_volume":4.21653420283E9}]}]}]}],"collapsed?":False}]}]}]}]}]}],"collapsed?":False}]}]}],"collapsed?":False}]}]}]}]}
  expected_algo = ('algo', 'hwrdr - TQQQ For The Long Term (Reddit Post Link)', ('wteq', (('wteq', (('ifelse', ('gt', ('now', ('asset', 'SPY')), ('ma', ('asset', 'SPY'), 200)), ('wteq', (('ifelse', ('gt', ('rsi', ('asset', 'TQQQ'), 10), ('number', 79.0)), ('asset', 'VIXY'), ('wteq', (('ifelse', ('gt', ('rsi', ('asset', 'SPXL'), 10), ('number', 80.0)), ('asset', 'VIXY'), ('wteq', (('asset', 'TQQQ'),))),))),)), ('wteq', (('ifelse', ('lt', ('rsi', ('asset', 'TQQQ'), 10), ('number', 31.0)), ('asset', 'TECL'), ('wteq', (('ifelse', ('lt', ('rsi', ('asset', 'SPY'), 10), ('number', 30.0)), ('asset', 'UPRO'), ('wteq', (('ifelse', ('lt', ('now', ('asset', 'TQQQ')), ('ma', ('asset', 'TQQQ'), 20)), ('wteq', (('filter', (('asset', 'SQQQ'), ('asset', 'TLT')), ('rsi', 10), ('top', 1)),)), ('wteq', (('ifelse', ('lt', ('rsi', ('asset', 'SQQQ'), 10), ('number', 31.0)), ('asset', 'SQQQ'), ('asset', 'TQQQ')),))),))),))),))),)),)), ('rebalance', 'daily'))
  algo = parse(symphony_json)

  assert algo == expected_algo

def test_parse_symph_rentech():
  #hwrdr - TQQQ For The Long Term (Reddit Post Link)
  #https://backtest-api.composer.trade/api/v1/public/symphonies/wmDK13UrFbWbObhmnQLG/score
  #
  # blocks: groups
  # indicator: cr, mar
  # sorts: ma, rsi
  # comparators: lte, gte
  symphony_json = {"id":"wmDK13UrFbWbObhmnQLG","step":"root","name":"hwrdr - TQQQ For The Long Term (Reddit Post Link)","description":"","rebalance":"daily","children":[{"id":"55d4cd1f-e631-48f9-9ec0-fa9d66e4ccee","step":"wt-cash-equal","children":[{"id":"5a12f26b-f2c9-4a88-8bb3-067557426e5e","step":"wt-cash-equal","children":[{"weight":{"num":100,"den":100},"id":"9a471655-8344-40b1-a26c-4d2267c73758","step":"if","children":[{"children":[{"id":"9ab6e988-d8df-48a8-b8e2-558c7525bffc","step":"wt-cash-equal","children":[{"id":"83ac7f18-f51b-4f0c-81fe-a13af8b8e399","step":"if","children":[{"children":[{"ticker":"VIXY","exchange":"BATS","name":"ProShares VIX Short-Term Futures ETF","id":"25928b5e-4d61-4650-a0f9-390bf7c73917","step":"asset","children-count":0}],"is-else-condition?":False,"rhs-fixed-value?":True,"lhs-fn":"relative-strength-index","lhs-window-days":"10","lhs-val":"TQQQ","id":"50d39ec5-0d69-4b0a-b637-36d51dd61b39","comparator":"gt","rhs-val":"79","step":"if-child","collapsed?":False},{"id":"70c7eadb-4b31-460f-907b-71e31da2c743","step":"if-child","is-else-condition?":True,"children":[{"id":"965ede5c-c51c-4f55-ab5e-afac5b48bc9e","step":"wt-cash-equal","children":[{"id":"f71d63f0-ce6b-4265-b880-f059d2a5b981","step":"if","children":[{"children":[{"ticker":"VIXY","exchange":"BATS","name":"ProShares VIX Short-Term Futures ETF","id":"c75e8db3-2de1-430a-986c-c2673276c246","step":"asset","children-count":0}],"is-else-condition?":False,"rhs-fixed-value?":True,"lhs-fn":"relative-strength-index","lhs-window-days":"10","lhs-val":"SPXL","id":"d5195b59-4a4f-43f3-8de4-e1d4a6c1da29","comparator":"gt","rhs-val":"80","step":"if-child"},{"id":"805cbb4e-2952-4c3a-bc81-1d01481bee23","step":"if-child","is-else-condition?":True,"children":[{"id":"7a62b727-a046-4535-ac8e-d48371d2db3c","step":"wt-cash-equal","children":[{"name":"ProShares UltraPro QQQ","ticker":"TQQQ","has_marketcap":False,"id":"c0145c27-f597-4caa-8c03-d2c417bdc8e9","exchange":"XNAS","price":18.92,"step":"asset","dollar_volume":5.535417683400001E9}]}]}]}],"collapsed?":False}]}]}]}],"rhs-fn":"moving-average-price","is-else-condition?":False,"lhs-fn":"current-price","rhs-window-days":"200","lhs-val":"SPY","id":"2c6de17e-d41b-41b4-b458-7a734b817c0a","comparator":"gt","rhs-val":"SPY","step":"if-child","collapsed?":False},{"id":"fbe0943b-8ac2-4100-ab0e-e3bbed88118e","step":"if-child","is-else-condition?":True,"children":[{"id":"46362f5a-a635-4b8a-90cb-4121419f62b3","step":"wt-cash-equal","children":[{"id":"988d50db-dd89-4cde-bfb3-b5d4553a29bf","step":"if","children":[{"children":[{"name":"Direxion Daily Technology Bull 3x Shares","ticker":"TECL","has_marketcap":False,"id":"d8a55927-4216-46d3-a079-99d86afbc0ab","exchange":"ARCX","price":23.24,"step":"asset","dollar_volume":1.293694108E8}],"is-else-condition?":False,"rhs-fixed-value?":True,"lhs-fn":"relative-strength-index","lhs-window-days":"10","lhs-val":"TQQQ","id":"504f7192-56a7-4470-aee6-728862893239","comparator":"lt","rhs-val":"31","step":"if-child","collapsed?":False},{"id":"9656f3e7-a985-49d9-b892-8c87e268d09a","step":"if-child","is-else-condition?":True,"children":[{"id":"05e69978-544d-40a6-a6cd-ecebb93eeb56","step":"wt-cash-equal","children":[{"id":"022d6bcf-28c4-42bd-a3fc-26b27b7af070","step":"if","children":[{"children":[{"name":"ProShares UltraPro S&P500","ticker":"UPRO","has_marketcap":False,"id":"c2582e3d-56d7-4a14-ba9c-70f998552301","exchange":"ARCX","price":28.41,"step":"asset","dollar_volume":5.2527686514E8}],"is-else-condition?":False,"rhs-fixed-value?":True,"lhs-fn":"relative-strength-index","lhs-window-days":"10","lhs-val":"SPY","id":"4c87e5ce-9795-4540-a2c3-0a915a8e6932","comparator":"lt","rhs-val":"30","step":"if-child","collapsed?":False},{"id":"30644bcf-e126-4449-9a80-b27b18983aea","step":"if-child","is-else-condition?":True,"children":[{"id":"af77345e-331b-4c3e-875c-516b4d81d7c7","step":"wt-cash-equal","children":[{"id":"bcc2169b-136e-4a86-b119-35bca8dc7d40","step":"if","children":[{"children":[{"id":"74c0023a-a50e-4edd-b0fa-167ad27a64ed","step":"wt-cash-equal","children":[{"select?":True,"children":[{"name":"ProShares UltraPro Short QQQ","ticker":"SQQQ","has_marketcap":False,"id":"2982fba0-5713-45be-9b7a-43fd69133a6c","exchange":"XNAS","price":61.32,"step":"asset","dollar_volume":9.65597774064E9},{"name":"iShares 20+ Year Treasury Bond ETF","ticker":"TLT","has_marketcap":False,"id":"f1d68991-9911-40ff-a217-d56ffcf2de97","exchange":"XNAS","price":105.7,"step":"asset","dollar_volume":1.3700322412E9,"children-count":0}],"select-fn":"top","select-n":"1","sort-by-fn":"relative-strength-index","sort-by-window-days":"10","id":"c89738ea-0bae-4fbb-94f1-aef5048fe10b","sort-by?":True,"step":"filter"}]}],"rhs-fn":"moving-average-price","is-else-condition?":False,"lhs-fn":"current-price","rhs-window-days":"20","lhs-val":"TQQQ","id":"b5ce2d31-5cf6-47f8-87de-f7bfb12f391d","comparator":"lt","rhs-val":"TQQQ","step":"if-child","collapsed?":False},{"id":"d0326c58-73d6-49c1-8162-7590cc5544bd","step":"if-child","is-else-condition?":True,"children":[{"id":"fce80c8a-8bdc-4afc-a547-dbb077ad2ad9","step":"wt-cash-equal","children":[{"id":"c010620b-9806-487e-8e36-b4cd8fa61671","step":"if","children":[{"children":[{"name":"ProShares UltraPro Short QQQ","ticker":"SQQQ","has_marketcap":False,"id":"9f7a293e-5a17-43f7-921d-6040e5933ab7","exchange":"XNAS","price":61.32,"step":"asset","dollar_volume":9.65597774064E9}],"is-else-condition?":False,"rhs-fixed-value?":True,"lhs-fn":"relative-strength-index","lhs-window-days":"10","lhs-val":"SQQQ","id":"87865f18-5bce-4e05-bb3c-bec089cd27da","comparator":"lt","rhs-val":"31","step":"if-child"},{"id":"ec8b8901-9652-407f-85a7-d82f1d01a311","step":"if-child","is-else-condition?":True,"children":[{"name":"ProShares UltraPro QQQ","ticker":"TQQQ","has_marketcap":False,"id":"cffede64-5415-44d4-a9b2-9c98d1ac8af4","exchange":"XNAS","price":21.73,"step":"asset","dollar_volume":4.21653420283E9}]}]}]}],"collapsed?":False}]}]}]}]}]}],"collapsed?":False}]}]}],"collapsed?":False}]}]}]}]}
  expected_algo = ('algo', 'hwrdr - TQQQ For The Long Term (Reddit Post Link)', ('wteq', (('wteq', (('ifelse', ('gt', ('now', ('asset', 'SPY')), ('ma', ('asset', 'SPY'), 200)), ('wteq', (('ifelse', ('gt', ('rsi', ('asset', 'TQQQ'), 10), ('number', 79.0)), ('asset', 'VIXY'), ('wteq', (('ifelse', ('gt', ('rsi', ('asset', 'SPXL'), 10), ('number', 80.0)), ('asset', 'VIXY'), ('wteq', (('asset', 'TQQQ'),))),))),)), ('wteq', (('ifelse', ('lt', ('rsi', ('asset', 'TQQQ'), 10), ('number', 31.0)), ('asset', 'TECL'), ('wteq', (('ifelse', ('lt', ('rsi', ('asset', 'SPY'), 10), ('number', 30.0)), ('asset', 'UPRO'), ('wteq', (('ifelse', ('lt', ('now', ('asset', 'TQQQ')), ('ma', ('asset', 'TQQQ'), 20)), ('wteq', (('filter', (('asset', 'SQQQ'), ('asset', 'TLT')), ('rsi', 10), ('top', 1)),)), ('wteq', (('ifelse', ('lt', ('rsi', ('asset', 'SQQQ'), 10), ('number', 31.0)), ('asset', 'SQQQ'), ('asset', 'TQQQ')),))),))),))),))),)),)), ('rebalance', 'daily'))
  algo = parse(symphony_json)

  assert algo == expected_algo

def test_parse_symph_basic_ifelse():
  #Test: rsi(SPY, 10) > 60 BIL vs TQQQ
  #https://backtest-api.composer.trade/api/v1/public/symphonies/rrkugCKc0HW4WpnPZegx/score
  #
  # blocks: wteq, ifelse
  # indicator: rsi, number
  # comparators: gt
  symphony_json = {'step': 'root', 'name': 'Test: rsi(SPY, 10) > 60 BIL vs TQQQ', 'description': '(Created with Composer AI)', 'rebalance': 'daily', 'children': [{'step': 'wt-cash-equal', 'children': [{'step': 'if', 'children': [{'children': [{'ticker': 'BIL', 'exchange': 'ARCX', 'name': 'SPDR Bloomberg 1-3 Month T-Bill ETF', 'step': 'asset', 'id': '2483d152-a495-47a4-8584-49e68afa605b', 'children-count': 0}], 'lhs-fn-params': {'window': 10}, 'rhs-fn': 'moving-average-price', 'is-else-condition?': False, 'rhs-fixed-value?': True, 'lhs-fn': 'relative-strength-index', 'lhs-val': 'SPY', 'id': 'a798eba4-de1a-4a47-801c-794bc38e3ee6', 'rhs-fn-params': {'window': 200}, 'comparator': 'gt', 'rhs-val': '60', 'step': 'if-child'}, {'step': 'if-child', 'id': '1998bbca-7947-4e4d-af9e-5d7b1b8cda62', 'is-else-condition?': True, 'children': [{'ticker': 'TQQQ', 'exchange': 'XNAS', 'name': 'ProShares UltraPro QQQ', 'step': 'asset', 'id': 'fb9932c3-2f55-4c8e-9241-8cba47d483ba', 'children-count': 0}]}], 'id': '0686332a-b1b9-4a63-9032-f912aafbbe95'}], 'id': 'ed578e5c-06fc-4516-8afb-b19de5020be8'}], 'id': 'rrkugCKc0HW4WpnPZegx'}
  expected_algo =  ('algo', 'Test: rsi(SPY, 10) > 60 BIL vs TQQQ', ('wteq', (('ifelse', ('gt', ('rsi', ('asset', 'SPY'), 10), ('number', 60.0)), ('asset', 'BIL'), ('asset', 'TQQQ')),)), ('rebalance', 'daily'))
  algo = parse(symphony_json)

  assert algo == expected_algo

def test_parse_root():
  symphony_json = {'step': 'root', 'children': [
      {'step': 'asset', 'ticker': 'asset1'},

      # root assumes that it only has 1 child
      # "asset2" should not exist in the result
      {'step': 'asset', 'ticker': 'asset2'}
    ]
  }
  expected_algo = ('algo', '', ('asset', 'asset1'), ('rebalance', 'none-set'))
  algo = parse(symphony_json)

  assert algo == expected_algo

def test_parse_wteq():
  symphony_json = {'step': 'wt-cash-equal', 'children': [
      {'step': 'asset', 'ticker': 'asset1'},
      {'step': 'asset', 'ticker': 'asset2'}
    ]}
  expected_algo = ('wteq', (('asset', 'asset1'), ('asset', 'asset2')))
  algo = parse(symphony_json)

  assert algo == expected_algo

def test_parse_wtspec():
  symphony_json = {'step': 'root', 'children': [{'step': 'wt-cash-specified', 'children': [{'weight': {'num': '90', 'den': 100}, 'ticker': 'asset1', 'step': 'asset'}, {'ticker': 'asset2', 'step': 'asset', 'weight': {'num': 10, 'den': 100}}]}]}
  expected_algo = ('algo', '', ('wtspec', (('asset', 'asset1'), ('asset', 'asset2')), ((90, 100), (10, 100))), ('rebalance', 'none-set'))

  algo = parse(symphony_json)

  assert algo == expected_algo

def test_parse_wtinvol():
  symphony_json = {'step': 'root', 'children': [{'step': 'wt-inverse-vol', 'window-days': 10, 'children': [{'ticker': 'asset1', 'step': 'asset'}, {'ticker': 'asset2', 'step': 'asset'}]}]}
  expected_algo = ('algo', '', ('wtinvol', (('asset', 'asset1'), ('asset', 'asset2')), 10), ('rebalance', 'none-set'))

  algo = parse(symphony_json)

  assert algo == expected_algo

def test_parse_ifelse():
  symphony_json = {'step': 'if', 'children': [
    {'step': 'if-child',
      'comparator': 'gt',
      'lhs-fn': 'current-price',
      'lhs-val':	'ifasset1',
      'rhs-fn': 'moving-average-price',
      'rhs-window-days': 200,
      'rhs-val': 'ifasset2',
      'children': [
        {'step': 'asset', 'ticker': 'asset1a'},

        # if-child assumes that it only has 1 child.
        # "asset1b" should not exist in the result
        {'step': 'asset', 'ticker': 'asset1b'}
      ]
    },

    {'step': 'if-child',
      'children': [
        {'step': 'asset', 'ticker': 'asset2a'},

        # if-child assumes that it only has 1 child.
        # "asset2b" should not exist in the result
        {'step': 'asset', 'ticker': 'asset2b'}
      ]
    },

    # if assumes that it only has 2 child
    # "asset3" should not exist in the result
    {'step': 'asset', 'ticker': 'asset3'}
  ]}

  expected_algo = ('ifelse',
    ('gt', ('now', ('asset', 'ifasset1')), ('ma', ('asset', 'ifasset2'), 200)),
    ('asset', 'asset1a'), 
    ('asset', 'asset2a'))

  algo = parse(symphony_json)

  assert algo == expected_algo

def test_parse_asset():
  symphony_json = {'step': 'asset', 'ticker': 'asset1'}
  expected_algo = ('asset', 'asset1')
  algo = parse(symphony_json)

  assert algo == expected_algo

def test_parse_wteq():
  symphony_json = {'step': 'wt-cash-equal', 'children': [
      {'step': 'asset', 'ticker': 'asset1'},
      {'step': 'asset', 'ticker': 'asset2'}
    ]}
  expected_algo = ('wteq', (('asset', 'asset1'), ('asset', 'asset2')))
  algo = parse(symphony_json)

  assert algo == expected_algo

def test_parse_filter():
  symphony_json = {'step': 'filter',
    'sort-by-fn': 'relative-strength-index',
    'sort-by-window-days': 15,
    'select-fn': 'top',
    'select-n': 2,
    'children': [
      {'step': 'asset', 'ticker': 'asset1'},
      {'step': 'asset', 'ticker': 'asset2'},
      {'step': 'asset', 'ticker': 'asset3'}
  ]}

  expected_algo = ('filter', (
      ('asset', 'asset1'),
      ('asset', 'asset2'),
      ('asset', 'asset3')
    ),
    ('rsi', 15),
    ('top', 2)
  )

  algo = parse(symphony_json)

  assert algo == expected_algo

def test_parse_group():
  symphony_json = {'step': 'group', 'name': 'Foo', 'children': [
      {'step': 'asset', 'ticker': 'asset1'},
      {'step': 'asset', 'ticker': 'asset2'}
    ]}
  expected_algo = ('group', 'Foo', ('wteq', (('asset', 'asset1'), ('asset', 'asset2'))))
  algo = parse(symphony_json)

  assert algo == expected_algo

def test_rebalance_period():
  symphony_json = {'step': 'root', 'name': 'Test Threshold', 'rebalance': 'daily', 'children': [{'step': 'wt-cash-equal', 'children': [{'weight': {'num': 100, 'den': 100}, 'ticker': 'BIL', 'step': 'asset'}]}]}

  expected_algo = ('algo', 'Test Threshold', ('wteq', (('asset', 'BIL'),)), ('rebalance', 'daily'))
  algo = parse(symphony_json)

  assert algo == expected_algo

def test_rebalance_threshold():
  symphony_json = {'step': 'root', 'name': 'Test Threshold', 'rebalance': 'none', 'rebalance-corridor-width': 0.1, 'children': [{'step': 'wt-cash-equal', 'children': [{'weight': {'num': 100, 'den': 100}, 'ticker': 'BIL', 'step': 'asset'}]}]}

  expected_algo = ('algo', 'Test Threshold', ('wteq', (('asset', 'BIL'),)), ('threshold', 0.1))
  algo = parse(symphony_json)

  assert algo == expected_algo

def test_rebalance_period_and_threshold():
  # period should take precedence over threshold. Threshold should only be used if rebalance value is "none"
  symphony_json = {'step': 'root', 'name': 'Test Threshold', 'rebalance-corridor-width': 0.1, 'children': [{'step': 'wt-cash-equal', 'children': [{'weight': {'num': 100, 'den': 100}, 'ticker': 'BIL', 'step': 'asset'}]}]}

  expected_algo = ('algo', 'Test Threshold', ('wteq', (('asset', 'BIL'),)), ('rebalance', 'none-set'))
  algo = parse(symphony_json)

  assert algo == expected_algo