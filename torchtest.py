import time
import torch
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def get_stock_data(tickers, start_date, end_date):
    data = {}
    failed_tickers = []
    
    for ticker in tickers:
        try:
            stock = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=False)
            if len(stock) > 0:  # Check if we got any data
                data[ticker] = stock['Adj Close'].values
            else:
                failed_tickers.append(ticker)
        except Exception as e:
            print(f"Error fetching {ticker}: {str(e)}")
            failed_tickers.append(ticker)
    
    if failed_tickers:
        print(f"\nFailed to fetch data for {len(failed_tickers)} tickers: {', '.join(failed_tickers)}")
    
    print(f"Successfully fetched data for {len(data)} tickers")
    return data

def get_window_sizes():
    """Generate a list of window sizes for analysis"""
    return [5, 10, 15, 20, 30, 45, 60, 90, 120, 180, 252]  # 252 is roughly one trading year

def calculate_rolling_returns(prices_dict, windows=None):
    if windows is None:
        windows = get_window_sizes()
    
    device = torch.device("mps") # if torch.backends.mps.is_available() else torch.device("cpu")
    
    # Convert all price series to a single tensor [n_tickers, n_timesteps]
    tickers = list(prices_dict.keys())
    max_length = max(len(prices) for prices in prices_dict.values())
    
    # Create padded tensor for all price series
    prices_tensor = torch.zeros((len(tickers), max_length), dtype=torch.float32, device=device)
    for i, ticker in enumerate(tickers):
        prices = prices_dict[ticker]
        prices_tensor[i, :len(prices)] = torch.tensor(prices, dtype=torch.float32)
    
    returns_dict = {}
    
    # Process all windows in a single operation
    all_returns = torch.zeros((len(windows), len(tickers), max_length), device=device)
    
    for i, window in enumerate(windows):
        future_values = prices_tensor[:, window:]
        past_values = prices_tensor[:, :-window]
        
        returns = (future_values - past_values) / past_values
        all_returns[i, :, window:] = returns
    
    # Calculate RSI
    rsi_results = calculate_rsi(prices_tensor, periods=[10, 14, 20, 25], device=device)
    
    # Move results back to CPU and organize into the original dictionary structure
    all_returns = all_returns.cpu().numpy()
    
    for ticker_idx, ticker in enumerate(tickers):
        ticker_returns = {}
        for window_idx, window in enumerate(windows):
            ticker_returns[f'{window}d'] = all_returns[window_idx, ticker_idx]
        
        # Add RSI results
        for period in [10, 14, 20]:
            ticker_returns[f'rsi_{period}d'] = rsi_results[f'rsi_{period}d'][ticker_idx].cpu().numpy()
        
        returns_dict[ticker] = ticker_returns
    
    return returns_dict

def calculate_rolling_returns_cpu(prices_dict, windows=None):
    """Calculate rolling returns using numpy (CPU only)"""
    if windows is None:
        windows = get_window_sizes()
        
    returns_dict = {}
    
    # Calculate returns and RSI for each ticker
    for ticker, prices in prices_dict.items():
        # Calculate returns for each window
        ticker_returns = {}
        prices_array = np.array(prices, dtype=np.float32)
        
        for window in windows:
            rolling_returns = np.zeros_like(prices_array)
            rolling_returns[window:] = (prices_array[window:] - prices_array[:-window]) / prices_array[:-window]
            ticker_returns[f'{window}d'] = rolling_returns
        
        # Calculate RSI
        rsi_dict = calculate_rsi_cpu({ticker: prices}, periods=[10, 14, 20, 25])[ticker]
        ticker_returns.update(rsi_dict)
        
        returns_dict[ticker] = ticker_returns
    
    return returns_dict

def calculate_rsi(prices_tensor, periods=[10, 14, 20], device=None):
    """Calculate RSI for multiple periods using PyTorch"""
    if device is None:
        device = prices_tensor.device
    
    # Calculate daily price changes
    price_changes = prices_tensor[:, 1:] - prices_tensor[:, :-1]
    
    rsi_results = {}
    for period in periods:
        # Create tensors for gains and losses
        gains = torch.zeros_like(price_changes)
        losses = torch.zeros_like(price_changes)
        
        # Separate gains and losses
        gains[price_changes > 0] = price_changes[price_changes > 0]
        losses[price_changes < 0] = -price_changes[price_changes < 0]
        
        # Calculate average gains and losses using exponential moving average
        alpha = 1.0 / period
        avg_gains = torch.zeros_like(gains)
        avg_losses = torch.zeros_like(losses)
        
        # First value is simple average
        avg_gains[:, period-1] = torch.mean(gains[:, :period], dim=1)
        avg_losses[:, period-1] = torch.mean(losses[:, :period], dim=1)
        
        # Calculate subsequent values using exponential moving average
        for i in range(period, gains.shape[1]):
            avg_gains[:, i] = (avg_gains[:, i-1] * (period-1) + gains[:, i]) / period
            avg_losses[:, i] = (avg_losses[:, i-1] * (period-1) + losses[:, i]) / period
        
        # Calculate RS and RSI
        rs = avg_gains / (avg_losses + 1e-10)  # Add small constant to avoid division by zero
        rsi = 100 - (100 / (1 + rs))
        
        # Pad the beginning to match original data length
        padded_rsi = torch.zeros((rsi.shape[0], prices_tensor.shape[1]), device=device)
        padded_rsi[:, period:] = rsi[:, period-1:]
        
        rsi_results[f'rsi_{period}d'] = padded_rsi
    
    return rsi_results

def calculate_rsi_cpu(prices_dict, periods=[10, 14, 20]):
    """Calculate RSI using numpy (CPU version)"""
    rsi_dict = {}
    
    for ticker, prices in prices_dict.items():
        prices_array = np.array(prices, dtype=np.float32)
        price_changes = np.diff(prices_array)
        ticker_rsi = {}
        
        for period in periods:
            gains = np.zeros_like(price_changes)
            losses = np.zeros_like(price_changes)
            
            gains[price_changes > 0] = price_changes[price_changes > 0]
            losses[price_changes < 0] = -price_changes[price_changes < 0]
            
            avg_gains = np.zeros_like(gains)
            avg_losses = np.zeros_like(losses)
            
            # First value is simple average
            avg_gains[period-1] = np.mean(gains[:period])
            avg_losses[period-1] = np.mean(losses[:period])
            
            # Calculate subsequent values using exponential moving average
            for i in range(period, len(gains)):
                avg_gains[i] = (avg_gains[i-1] * (period-1) + gains[i]) / period
                avg_losses[i] = (avg_losses[i-1] * (period-1) + losses[i]) / period
            
            rs = avg_gains / (avg_losses + 1e-10)
            rsi = 100 - (100 / (1 + rs))
            
            # Pad the beginning to match original data length
            padded_rsi = np.zeros(len(prices_array))
            padded_rsi[period:] = rsi[period-1:]
            
            ticker_rsi[f'rsi_{period}d'] = padded_rsi
        
        rsi_dict[ticker] = ticker_rsi
    
    return rsi_dict

def generate_synthetic_data(n_tickers, n_days, seed=42):
    """
    Generate synthetic stock price data using geometric Brownian motion
    Parameters:
        n_tickers: number of synthetic tickers to generate
        n_days: number of days of data
        seed: random seed for reproducibility
    """
    np.random.seed(seed)
    
    # Parameters for synthetic data
    mu = np.random.normal(0.0001, 0.0002, n_tickers)  # Daily drift
    sigma = np.random.uniform(0.01, 0.02, n_tickers)  # Daily volatility
    initial_price = np.random.uniform(20, 200, n_tickers)  # Starting prices
    
    data = {}
    for i in range(n_tickers):
        # Generate daily returns using geometric Brownian motion
        returns = np.random.normal(mu[i], sigma[i], n_days)
        # Calculate cumulative returns
        cumulative_returns = np.exp(np.cumsum(returns))
        # Generate price series
        prices = initial_price[i] * cumulative_returns
        
        ticker = f'SYN{i:04d}'  # Synthetic ticker names: SYN0000, SYN0001, etc.
        data[ticker] = prices.astype(np.float32)
    
    return data

# Update the tickers list with 100 stocks
tickers = [
]

# Extend the time period to 2 years to get more data
end_date = datetime.now()
start_date = end_date - timedelta(days=365*2)  # Get 2 years of data

# Calculate how many days of data we have from yfinance
n_days = 1000

# Generate synthetic data
print("\nGenerating synthetic data...")
synthetic_prices = generate_synthetic_data(n_tickers=5000, n_days=n_days)

# Combine real and synthetic data
all_prices = {**synthetic_prices}
print(f"Total number of tickers: {len(all_prices)}")

# Run calculations multiple times to get better timing comparison
n_runs = 3
gpu_times = []
cpu_times = []

print("\nRunning performance comparison with combined real and synthetic data...")
for i in range(n_runs):
    print(f"\nRun {i+1}/{n_runs}")
    
    # GPU version
    start_time = time.time()
    rolling_returns_gpu = calculate_rolling_returns(all_prices)
    gpu_time = time.time() - start_time
    gpu_times.append(gpu_time)
    print(f"GPU time: {gpu_time:.4f} seconds")
    
    # CPU version
    start_time = time.time()
    rolling_returns_cpu = calculate_rolling_returns_cpu(all_prices)
    cpu_time = time.time() - start_time
    cpu_times.append(cpu_time)
    print(f"CPU time: {cpu_time:.4f} seconds")

# Print average times
print("\nPerformance Summary (with synthetic data):")
print(f"Average GPU time: {np.mean(gpu_times):.4f} seconds (±{np.std(gpu_times):.4f})")
print(f"Average CPU time: {np.mean(cpu_times):.4f} seconds (±{np.std(cpu_times):.4f})")
print(f"GPU speedup: {np.mean(cpu_times)/np.mean(gpu_times):.2f}x")

# Sample both real and synthetic tickers for verification
synthetic_samples = np.random.choice(list(synthetic_prices.keys()), 2, replace=False)
sample_tickers = np.concatenate([synthetic_samples])

# Verify results
windows = get_window_sizes()
for ticker in sample_tickers:
    for window in windows:
        np.testing.assert_allclose(
            rolling_returns_gpu[ticker][f'{window}d'],
            rolling_returns_cpu[ticker][f'{window}d'],
            rtol=1e-5
        )
print("\nResults match between GPU and CPU calculations!")

# Print sample results
print("\nSample results for real and synthetic tickers:")
for ticker in sample_tickers:
    print(f"\nRolling returns and RSI for {ticker} ({'synthetic'}):")
    print(f"Data points: {len(rolling_returns_gpu[ticker]['5d'])}")
    print(f"Sample 5-day returns: {rolling_returns_gpu[ticker]['5d'][5:10]}")
    print(f"Sample 14-day RSI: {rolling_returns_gpu[ticker]['rsi_14d'][14:19]}")
