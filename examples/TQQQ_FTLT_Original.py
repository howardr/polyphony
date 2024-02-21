import yfinance as yf
import pandas as pd
import pandas_ta as ta

# Copied from Walter.Sanders (whsmacon) in Dicord
# https://discord.com/channels/1018958699991138386/1019589796802351106/1191919999607132270

# Constants for the assets
ASSETS = ["SPY", "QQQ", "UVXY", "TLT", "UUP", "VIXY", "XLP", "SPLV", "TQQQ", "SOXL", "TECL", "UDOW", "UPRO", "FNGU", "BULZ", "SMH", "FNGS", "PSQ", "SQQQ", "DIA"]

# Function to fetch historical data for a given ticker
def fetch_data(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date)

# Function to calculate RSI
def calculate_rsi(data, window):
    return ta.rsi(data['Adj Close'], length=window)

# Function to calculate Simple Moving Average (SMA)
def calculate_sma(data, window):
    return ta.sma(data['Adj Close'], length=window)

# Function to decide the investment based on the provided logic

def decide_investment(data, dollar_amount):
    # Check for Bull Market or Bear Market conditions
    if data['SPY_current_price'] > data['SPY_sma_200']:
        # Bull Market conditions
        if data['QQQ_rsi_10'] > 80:
            return [("UVXY", dollar_amount)]
        elif data['SPY_rsi_10'] > 80:
            return [("UVXY", dollar_amount)]
        elif data['SPY_rsi_60'] > 60:
            # Select top asset based on 15-day moving average return
            top_assets = sorted(['TLT', 'UUP', 'VIXY', 'XLP', 'SPLV'], key=lambda x: data[f'{x}_ma_return_15'], reverse=True)[:1]
            allocation = [(asset, dollar_amount) for asset in top_assets]
            return allocation
        else:
            # Select top 3 assets based on 21-day moving average return
            top_assets = sorted(['TQQQ', 'SOXL', 'TECL', 'UDOW', 'UPRO', 'FNGU', 'BULZ'], key=lambda x: data[f'{x}_ma_return_21'], reverse=True)[:3]
            allocation = [(asset, dollar_amount * 0.67 / 3) for asset in top_assets]
            allocation.append(("SVXY", dollar_amount * 0.33))
            return allocation
    else:
        # Dip Buy Strategy or Bear Market Sideways Protection
        if data['TQQQ_rsi_10'] < 31:
            return [("TECL", dollar_amount)]
        elif data['SMH_rsi_10'] < 30:
            return [("SOXL", dollar_amount)]
        elif data['FNGS_rsi_10'] < 30:
            return [("FNGU", dollar_amount)]
        elif data['SPY_rsi_10'] < 30:
            return [("UPRO", dollar_amount)]
        else:
            # Bear Market Sideways Protection
            allocations = []
            if data['QQQ_cumulative_return_252'] < -20:
                # Nasdaq In Crash Territory, Time to Deleverage
                if data['QQQ_current_price'] < data['QQQ_sma_20']:
                    #this is verified
                    if data['QQQ_cumulative_return_60'] <= -12:
                        # Sideways Market Deleverage
                        if data['SPY_current_price'] > data['SPY_sma_20']:
                            allocations.append(("SPY", dollar_amount / 2))
                        else:
                            if data['TLT_rsi_10'] > data['SQQQ_rsi_10']:
                                allocations.append(("QQQ", dollar_amount / 2))
                            else:
                                allocations.append(("PSQ", dollar_amount / 2))
                            
                        if data['TLT_rsi_10'] > data['SQQQ_rsi_10']:
                            allocations.append(("QQQ", dollar_amount / 2))
                        else:
                            allocations.append(("PSQ", dollar_amount / 2))
                    else:
                        if data['TLT_rsi_10'] > data['SQQQ_rsi_10']:
                            allocations.append(("TQQQ", dollar_amount / 2))
                        else:
                            allocations.append(("SQQQ", dollar_amount / 2))
                else:
                    if data['SQQQ_rsi_10'] < 31:
                        allocations.append(("PSQ", dollar_amount / 2))
                    else:
                        if data['QQQ_cumulative_return_10'] > 5.5:
                            allocations.append(("PSQ", dollar_amount / 2))
                        else:
                            top_asset = sorted(['QQQ', 'SMH'], key=lambda x: data[f'{x}_rsi_10'], reverse=True)[0]
                            allocations.append((top_asset, dollar_amount / 2))
            else:
                #this is verified
                if data['QQQ_current_price'] < data['QQQ_sma_20']:
                    if data['TLT_rsi_10'] > data['SQQQ_rsi_10']:
                        allocations.append(("TQQQ", dollar_amount / 2))
                    else:
                        allocations.append(("SQQQ", dollar_amount / 2))
                else:
                    if data['SQQQ_rsi_10'] < 31:
                        allocations.append(("SQQQ", dollar_amount / 2))
                    else:
                        if data['QQQ_cumulative_return_10'] > 5.5:
                            allocations.append(("SQQQ", dollar_amount / 2))
                        else:
                            top_asset = sorted(['TQQQ', 'SOXL'], key=lambda x: data[f'{x}_rsi_10'], reverse=True)[0]
                            allocations.append((top_asset, dollar_amount / 2))

            # Additional branch for Bear Market Sideways Protection
            if data['QQQ_current_price'] < data['QQQ_sma_20']:
                if data['QQQ_cumulative_return_60'] <= -12:
                    # Sideways Market Deleverage
                    if data['SPY_current_price'] > data['SPY_sma_20']:
                        allocations.append(("SPY", dollar_amount / 2))
                    else:
                        if data['TLT_rsi_10'] > data['SQQQ_rsi_10']:
                            allocations.append(("QQQ", dollar_amount / 2))
                        else:
                            allocations.append(("PSQ", dollar_amount / 2))
                        
                    if data['TLT_rsi_10'] > data['SQQQ_rsi_10']:
                        allocations.append(("QQQ", dollar_amount / 2))
                    else:
                        allocations.append(("PSQ", dollar_amount / 2))
                else:
                    if data['TLT_rsi_10'] > data['SQQQ_rsi_10']:
                        allocations.append(("TQQQ", dollar_amount / 2))
                    else:
                        allocations.append(("SQQQ", dollar_amount / 2))
            else:
                # Additional branch based on RSI conditions
                if data['SQQQ_rsi_10'] < 31:
                    allocations.append(("SQQQ", dollar_amount / 2))
                else:
                    if data['QQQ_cumulative_return_70'] < -15:
                        top_asset = sorted(['TQQQ', 'SOXL'], key=lambda x: data[f'{x}_rsi_10'], reverse=True)[0]
                        allocations.append((top_asset, dollar_amount / 2))
                    else:
                        top_assets = sorted(['SPY', 'QQQ', 'DIA', 'XLP'], key=lambda x: data[f'{x}_cumulative_return_15'], reverse=True)[:2]
                        allocations += [(asset, dollar_amount / 4) for asset in top_assets]

            if not allocations:
                allocations.append(("TQQQ", dollar_amount))  # Default case if none of the above conditions are met
            return allocations


# Function to get recommendations based on a specific date and dollar amount

def get_recommendations(date, dollar_amount):
    end_date = pd.to_datetime(date)
    start_date = end_date - pd.DateOffset(months=14)  # Adjust as needed for historical data

    data = {}
    for asset in ASSETS:
        df = fetch_data(asset, start_date, end_date)

        # Current Price
        data[f'{asset}_current_price'] = df.iloc[-1]['Adj Close']

        # SMA - 200 days and 20 days
        data[f'{asset}_sma_200'] = calculate_sma(df, 200).iloc[-1]
        data[f'{asset}_sma_20'] = calculate_sma(df, 20).iloc[-1]

        # RSI - 10 days and 60 days
        data[f'{asset}_rsi_10'] = calculate_rsi(df, 10).iloc[-1]
        data[f'{asset}_rsi_60'] = calculate_rsi(df, 60).iloc[-1]

        # Cumulative Returns - 252 days, 70 days, 60 days, and 10 days
        data[f'{asset}_cumulative_return_252'] = df['Adj Close'].pct_change(252).iloc[-1] * 100
        data[f'{asset}_cumulative_return_70'] = df['Adj Close'].pct_change(70).iloc[-1] * 100
        data[f'{asset}_cumulative_return_60'] = df['Adj Close'].pct_change(60).iloc[-1] * 100
        data[f'{asset}_cumulative_return_15'] = df['Adj Close'].pct_change(15).iloc[-1] * 100
        data[f'{asset}_cumulative_return_10'] = df['Adj Close'].pct_change(10).iloc[-1] * 100

        # Moving Average Returns - 15 days and 21 days
        data[f'{asset}_ma_return_15'] = df['Adj Close'].pct_change().rolling(window=15).mean().iloc[-1] * 100
        data[f'{asset}_ma_return_21'] = df['Adj Close'].pct_change().rolling(window=21).mean().iloc[-1] * 100

    return decide_investment(data, dollar_amount)


# Main execution block
if __name__ == "__main__":
    date_input = input("Enter a date (YYYY-MM-DD) or leave blank for today: ")
    dollar_amount_input = input("Enter the dollar amount or leave blank for 10,000: ")

    date = pd.to_datetime(date_input) if date_input else pd.Timestamp.today()
    date = date + pd.DateOffset(days=1)  # Adjust for data availability

    dollar_amount_input = float(dollar_amount_input) if dollar_amount_input else 10000

    recommendations = get_recommendations(date, dollar_amount_input)

    for ticker, amount in recommendations:
        print(f"Invest ${amount:.2f} in {ticker}")
