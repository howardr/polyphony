import datetime
import json
import pandas as pd
import src.utils as utils
import traceback
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from src.allocate import allocate, preprocess, run_indicator
from src.parse import parse
import src.composer as composer
import os

tiingo_api_key = os.getenv('TIINGO_API_KEY')
if not tiingo_api_key:
    raise ValueError("TIINGO_API_KEY environment variable is not set")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

def fetch_tiingo_data(tickers, start_date, end_date):
    """
    Fetch historical price data from Tiingo and format it similar to yfinance
    """

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {tiingo_api_key}'
    }
    
    all_data = {}
    for ticker in tickers:
        url = f'https://api.tiingo.com/tiingo/daily/{ticker}/prices'
        params = {
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'format': 'json'
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            # Convert to DataFrame
            df = pd.DataFrame(data)
            df.set_index('date', inplace=True)
            df.index = pd.to_datetime(df.index)
            # Rename columns to match yfinance format
            df = df.rename(columns={
                'adjClose': 'Adj Close',
                'adjOpen': 'Open',
                'adjHigh': 'High',
                'adjLow': 'Low',
                'adjVolume': 'Volume'
            })
            all_data[ticker] = df
    
    # Combine all tickers into a single DataFrame with MultiIndex
    combined = pd.concat({ticker: all_data[ticker] for ticker in tickers}, axis=1)
    # Reorder levels to match yfinance output
    combined = combined.reorder_levels([1, 0], axis=1)
    return combined

@app.route('/history/indicator', methods=['POST'])
def get_algo_results():
    try:
        indicator = request.form.get('indicator')
        if not indicator:
            return jsonify({'error': 'Indicator is required'}), 400

        # Get start and finish dates from request parameters
        start_str = request.form.get('start')
        finish_str = request.form.get('finish')
        
        if not start_str or not finish_str:
            return jsonify({'error': 'Start and finish dates are required'}), 400

        try:
            start_date = datetime.datetime.strptime(start_str, '%Y-%m-%d').date()
            finish_date = datetime.datetime.strptime(finish_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        if start_date > finish_date:
            return jsonify({'error': 'Start date must be before finish date'}), 400

        # Parse the indicator
        parsed_indicator = json.loads(indicator)

        if parsed_indicator[0] == "number":
            # Generate business days between start and finish
            date_range = pd.bdate_range(start=start_date, end=finish_date, tz='UTC')
            
            return jsonify({
                'indicator': indicator,
                'results': [{
                    'result': parsed_indicator[1],
                    'timestamp': d.strftime('%Y-%m-%d')
                } for d in date_range]
            })

        summary = preprocess(parsed_indicator)
        tickers = summary["assets"]

        # Adjust start date to account for indicator's window requirements
        adjusted_start = utils.subtract_trading_days(start_date, summary["max_window_days"])
        price_data = fetch_tiingo_data(
            list(tickers),
            adjusted_start,
            finish_date + datetime.timedelta(days=1)
        )

        # Use the date range between start and finish
        date_range = price_data.index[price_data.index >= pd.Timestamp(start_date).tz_localize('UTC')]
        df = pd.DataFrame(0.0, index=date_range, columns=["value"])

        cache_data = {}
        for r in date_range:
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
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/algo/<id>', methods=['GET'])
def get_algo(id):
    try:
        # Fetch the composer definition using the ID
        definition = composer.fetch_definition(id)
        if not definition:
            return jsonify({'error': 'Algorithm not found'}), 404

        # Parse the definition into our internal format
        parsed_algo = parse(definition)
        
        # Get summary info about the algorithm
        summary = preprocess(parsed_algo)
        
        # Convert sets to lists in summary
        json_summary = {
            'assets': list(summary['assets']),
            'investable_assets': list(summary['investable_assets']),
            'max_window_days': summary['max_window_days']
        }

        return jsonify({
            'id': id,
            'name': definition.get('name', ''),
            'description': definition.get('description', ''),
            'algo': parsed_algo,
            'summary': json_summary
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))  # Default to 5000 if PORT not set
    debug = os.getenv('PROD', 'false').lower() != 'true'  # Debug mode on unless PROD=true
    
    app.run(
        host='0.0.0.0',  # Listen on all available interfaces
        port=port,
        debug=debug
    )