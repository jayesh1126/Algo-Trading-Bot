import pandas as pd
import os
from binance.client import Client
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Set the API key and secret
api_key = "key"
api_secret = "key"

# Set the Binance API URL and connect to the client
client = Client(api_key, api_secret)
client.API_URL = 'https://testnet.binance.vision/api'

# Set the directory path where your CSV files are stored
directory = 'C:/Users/jonat/Documents/crypto/spot/monthly/klines/XRPBNB/1d'

# Define the columns to use for scaling and training the model
cols = ['Open', 'High', 'Low', 'Volume', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume']

# Create an empty DataFrame to store the concatenated data
concatenated_df = pd.DataFrame()

# Iterate through each CSV file in the directory and concatenate them
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        # Read the CSV file into a DataFrame
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath, header=None, names=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
        
        # Append the DataFrame to the concatenated DataFrame
        concatenated_df = pd.concat([concatenated_df, df])

# Preprocess the concatenated data
concatenated_df.drop('Ignore', axis=1, inplace=True)
cols_to_scale = [col for col in cols if col != 'Close'] # Only scale columns other than 'Close'
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(concatenated_df[cols_to_scale])
scaled_df = pd.DataFrame(scaled_data, columns=cols_to_scale)


# Split the data into training and testing sets
print(scaled_df.columns)
X = scaled_df.drop('Close', axis=1)
y = scaled_df.drop('Close', axis=1)['Open']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)


# Remove the 'Close' column from the X_train DataFrame
X_train = X_train.drop('Close', axis=1)

# Create a linear regression model
model = LinearRegression()

# Train the model on the training data
model.fit(X_train, y_train)

# Get the latest close price from Binance
coin_price = client.get_symbol_ticker(symbol="XRPBNB")['price']

# Scale the latest close price and predict the next close price
latest_data = concatenated_df[cols].tail(1)
latest_scaled_data = scaler.transform(latest_data.drop('Close', axis=1))
next_close = model.predict(latest_scaled_data)[0]

# Calculate the Kelly criterion fraction
fraction = (next_close / float(coin_price) - 1) / (1 - next_close / float(coin_price))

# Implement the trading strategy
if fraction > 0 and fraction <= 1:
    print("Buy signal detected")
    # Buy logic
    # ...
elif fraction < 0:
    print("Sell signal detected")
    # Sell logic
    # ...
else:
    print("Hold signal detected")
    # Hold logic
    # ...