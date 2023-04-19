# Import necessary libraries
import pandas as pd
import numpy as np
from binance.client import Client
import os

# Set the API key and secret
api_key = "key"
api_secret = "key"

# Set the Binance API URL and connect to the client
client = Client(api_key, api_secret)

# Set the directory path where your CSV files are stored
directory_month = '<<insert_directory_here>>'
directory_day = '<<insert_directory_here>>'

# Define the columns to use for scaling and training the model
cols = ['Open', 'High', 'Low', 'Volume', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume','Close']

# Create an empty DataFrame to store the concatenated data
concatenated_df = pd.DataFrame()

# Iterate through each CSV file in the directory and concatenate them
for filename in os.listdir(directory_month):
    if filename.endswith(".csv"):
        # Read the CSV file into a DataFrame
        filepath = os.path.join(directory_month, filename)
        df = pd.read_csv(filepath, header=None, names=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])

        # Append the DataFrame to the concatenated DataFrame
        concatenated_df = pd.concat([concatenated_df, df])

for filename in os.listdir(directory_day):
    if filename.endswith(".csv"):
        # Read the CSV file into a DataFrame
        filepath = os.path.join(directory_day, filename)
        df = pd.read_csv(filepath, header=None, names=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])

        # Append the DataFrame to the concatenated DataFrame
        concatenated_df = pd.concat([concatenated_df, df])

# Get the raw data using Binance API
raw_data = client.get_klines(symbol="SOLUSDT", interval="1d", limit=200)

# Convert raw data into pandas dataframe
live_data = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

# Convert timestamp to datetime
live_data['timestamp'] = pd.to_datetime(live_data['timestamp'], unit='ms')

# Set timestamp as index
live_data = live_data.set_index('timestamp')

# Drop unnecessary columns from the live data
live_data.drop(['close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'], axis=1, inplace=True)

# Convert the data types of columns to float
live_data = live_data.astype(float)

# Concatenate the historical and live data
data = pd.concat([concatenated_df, live_data], axis=0)

# Drop duplicate data and reset index
data.drop_duplicates(subset=['Close'], inplace=True)
data.reset_index(drop=True, inplace=True)

# Define the Fibonacci retracement levels to use
fib_levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]

# Loop through each period in the data and calculate the high, low, and range
for i in range(len(data)):
    high = data['High'].iloc[i]
    low = data['Low'].iloc[i]
    range = high - low

    # Loop through each Fibonacci level and calculate the corresponding price level
    for level in fib_levels:
        price = high - range * level
        # Check if the current close price is above the current Fibonacci level
        if data['Close'].iloc[i] > price:
            print('Buy signal')
            break
        # Check if the current close price is below the current Fibonacci level
        elif data['Close'].iloc[i] < price:
            print('Sell signal')
            break
    else:
        print('Hold signal')

