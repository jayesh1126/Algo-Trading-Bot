import pandas as pd
import os
from binance.client import Client
# Set the API key and secret
api_key = "key"
api_secret = "key"

# Set the Binance API URL and connect to the client
client = Client(api_key, api_secret)


# Set the directory path where your CSV files are stored
directory_month = 'C:/Users/jayes/Documents/Algo Trading Project - Johnny/spot/monthly/klines/SOLUSDT/1d'
directory_day = 'C:/Users/jayes/Documents/Algo Trading Project - Johnny/spot/daily/klines/SOLUSDT/1d'

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
        # concatenated_df contains everything
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

#drop duplicate data and reset index
data.drop_duplicates(subset=['Close'], inplace=True)
data.reset_index(drop=True, inplace=True)



# Bollinger Bands: Bollinger Bands are a volatility indicator that uses a moving 
    # average and standard deviations to create a channel around the price. They can 
    # be used to identify potential buy or sell signals when the price moves outside 
    # of the channel.
def calculate_bollinger_bands(data, window, std):
    rolling_mean = data['Close'].rolling(window=window).mean()
    rolling_std = data['Close'].rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * std)
    lower_band = rolling_mean - (rolling_std * std)
    return rolling_mean, upper_band, lower_band

last_20_periods = concatenated_df[-20:]
rolling_mean, upper_band, lower_band = calculate_bollinger_bands(last_20_periods, 20, 2)

# Decision making, here .iloc[-1] accesses the last close value of the coin, but
# we will use the binance API to get the current value so we compare with the live current price
current_price = last_20_periods['Close'].iloc[-1]
if current_price > upper_band.iloc[-1]:
    print("Price is above the upper Bollinger Band, sell!")
elif current_price < lower_band.iloc[-1]:
    print("Price is below the lower Bollinger Band, buy!")
else:
    print("Price is within the Bollinger Bands, hold.")