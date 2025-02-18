import datetime
import json
import pandas as pd
import src.utils as utils
import traceback
import yfinance as yf
from flask import Flask, jsonify, request
from flask_cors import CORS
from src.allocate import allocate, preprocess, run_indicator
from src.parse import parse

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

@app.route('/history/indicator', methods=['POST'])
def get_algo_results():
    try:
        indicator = request.form.get('indicator')
        if not indicator:
            return jsonify({'error': 'Indicator is required'}), 400

        # Parse the indicator
        parsed_indicator = json.loads(indicator)
        summary = preprocess(parsed_indicator)
        tickers = summary["assets"]

        # bug fix. Need to have more than > 1 ticker
        if len(tickers) == 1:
          tickers = tickers.union(["QQQ"])

        num_days = 30
        date = datetime.date.today()

        start_date = utils.subtract_trading_days(date, summary["max_window_days"] + num_days)
        price_data = yf.download(
          " ".join(tickers),
          start=start_date,
          end=(date + datetime.timedelta(days=1)),
          progress=False
        )

        range = price_data.index[-num_days:]
        df = pd.DataFrame(0.0, index=range, columns=["value"])

        cache_data = {}
        for r in range:
          value = run_indicator(parsed_indicator, r, price_data, cache_data)
          df.at[r, "value"] = value

        # Format results
        formatted_results = [
          {
            'result': row[1],
            'timestamp': row[0].strftime('%Y-%m-%d')
          } for row in df.itertuples()
        ]
        
        return jsonify({
          'indicator': indicator,
          'results': formatted_results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
  app.run(debug=True)