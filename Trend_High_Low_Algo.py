import pandas as pd

# Load klines data from CSV file
data = pd.read_csv('spot/monthly/klines/SOLUSDT/1d/SOLUSDT-1d-2023-01.csv')

# Convert timestamp to datetime and set as index
data['Open Time'] = pd.to_datetime(data['Open Time'], unit='ms')
data.set_index('Open Time', inplace=True)

# Calculate SMA for last 30 days
sma = data['Close'].rolling(window=30).mean()

# Print SMA values
print(sma)


    # Relative Strength Index (RSI): The RSI is a momentum oscillator that measures 
    # the speed and change of price movements. It can be used to identify overbought and 
    # oversold conditions, as well as potential trend reversals.
def calculate_rsi(data, period=14):
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
# This function takes a Pandas DataFrame containing klines data and returns the Relative
#  Strength Index (RSI) calculated over a specified period. The default period is 14,
#  but you can adjust it to your liking.


    # Moving Average Convergence Divergence (MACD): The MACD is a trend-following 
    # momentum indicator that uses the difference between two exponential moving 
    # averages (EMAs) to identify changes in momentum. It can be used to identify trend 
    # changes and potential buy or sell signals.
def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    ema_fast = data['close'].ewm(span=fast_period, adjust=False).mean()
    ema_slow = data['close'].ewm(span=slow_period, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram
# This function takes a Pandas DataFrame containing klines data and returns 
# the Moving Average Convergence Divergence (MACD) and its associated signal line 
# and histogram values. The default fast period is 12, the slow period is 26, and 
# the signal period is 9, but you can adjust them to your liking.


    # Bollinger Bands: Bollinger Bands are a volatility indicator that uses a moving 
    # average and standard deviations to create a channel around the price. They can 
    # be used to identify potential buy or sell signals when the price moves outside 
    # of the channel.
def calculate_bollinger_bands(data, window=20, std=2):
    rolling_mean = data['close'].rolling(window=window).mean()
    rolling_std = data['close'].rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * std)
    lower_band = rolling_mean - (rolling_std * std)
    return upper_band, lower_band
# This function takes a Pandas DataFrame containing klines data and returns
# the upper and lower Bollinger Bands calculated over a specified window and 
# standard deviation. The default window is 20 and the default standard deviation is 
# 2, but you can adjust them to your liking.


    # Stochastic Oscillator: The Stochastic Oscillator is a momentum indicator 
    # that compares the closing price of a cryptocurrency to its price range over 
    # a certain period of time. It can be used to identify overbought and oversold 
    # conditions, as well as potential trend reversals.
def calculate_stochastic_oscillator(data, period=14):
    lowest_low = data['low'].rolling(window=period).min()
    highest_high = data['high'].rolling(window=period).max()
    k_percent = ((data['close'] - lowest_low) / (highest_high - lowest_low)) * 100
    d_percent = k_percent.rolling(window=3).mean()
    return k_percent, d_percent
# This function takes a Pandas DataFrame containing klines data and returns the
# Stochastic Oscillator %K and %D values calculated over a specified period. 
# The default period is 14, but you can adjust it to your liking.


    # Fibonacci Retracement: Fibonacci Retracement is a technical analysis tool
    # that uses horizontal lines to indicate areas of support or resistance at the 
    # key Fibonacci levels before the price continues in the original direction. 
    # It can be used to identify potential buy or sell signals at these levels.
def calculate_fibonacci_retracement(data, high, low):
    pivot = data['close'].iloc[-1]
    low_range = low - pivot
    high_range = high - pivot
    levels = [0.236, 0.382, 0.5, 0.618,0.786, 1.0]
    fib_levels = []
    for level in levels:
        fib_levels.append(pivot + (level * low_range))
        fib_levels.append(pivot + (level * high_range))
    return fib_levels
# This function takes a Pandas DataFrame containing klines data,
# as well as the highest and lowest price points over the specified period,
# and returns the Fibonacci retracement levels calculated based on the pivot point
# (the closing price of the most recent period), and the high and low range.
