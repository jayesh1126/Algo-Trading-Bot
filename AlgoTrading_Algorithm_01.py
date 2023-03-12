import pandas as pd
import os
from sklearn.tree import DecisionTreeClassifier
from binance.client import Client


# Define a function to generate the predictions for the DataFrame
def generate_predictions(df):
    predictions = []
    for i in range(len(df)):
        if i == 0:
            predictions.append(0)
        else:
            if df.iloc[i]['Close'] > df.iloc[i-1]['Close']:
                predictions.append(1)
            else:
                predictions.append(-1)
    return predictions


# Set the API key and secret
api_key = "key"
api_secret = "key"

# Set the Binance API URL and connect to the client
client = Client(api_key, api_secret)
client_live = Client()
client.API_URL = 'https://testnet.binance.vision/api'

# Set the directory path where your CSV files are stored
directory_month = 'C:/Users/jonat/Documents/crypto/spot/monthly/klines/SOLUSDT/1d'
directory_day = 'C:/Users/jonat/Documents/crypto/spot/daily/klines/SOLUSDT/1d'

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


# Add the 'Prediction' column to the DataFrame
concatenated_df['Prediction'] = generate_predictions(concatenated_df)


# Split the data into training and testing sets
train_size = int(len(concatenated_df) * 0.8)
train_df = concatenated_df[:train_size]
test_df = concatenated_df[train_size:]

# Extract the features and labels for the training and testing sets
train_X = train_df[cols]
train_y = train_df['Prediction']
test_X = test_df[cols]
test_y = test_df['Prediction']
test_X = test_X[train_X.columns]

# Get the current price of the cryptocurrency
ticker = 'SOLUSDT'
ticker_info = client_live.get_symbol_ticker(symbol=ticker)
current_price = float(ticker_info['price'])

# Create a DataFrame with the current price and historical data of the last row
last_row = concatenated_df.tail(1)
current_data = pd.DataFrame([last_row[cols].values.tolist()[0] + [current_price]], columns=cols+['x'])
current_data = current_data.drop(columns=['x'])

# Train the decision tree classifier
model = DecisionTreeClassifier()
model.fit(train_X, train_y)

# Define the parameters for the Kelly Criterion
win_rate = 0.5 # Winning probability of the trading strategy
payoff_ratio = 2 # The ratio of the potential profit to the potential loss
risk = 0.1 # The percentage of the portfolio that can be risked on a single trade

# Calculate the Kelly Criterion fraction
kelly_fraction = (win_rate * payoff_ratio - (1 - win_rate)) / payoff_ratio

# Make a prediction on whether to buy, sell or hold based on the machine learning model
prediction = model.predict(current_data)
print(prediction)

# Determine the position size based on the Kelly Criterion
balance = client.get_asset_balance(asset='USDT')
available_balance = float(balance['free'])
print("available balance", available_balance)
position_size = available_balance * kelly_fraction * risk / current_price

# Calculate the potential profit for the trade
if prediction == 1: # buy signal
    potential_profit = (1 + payoff_ratio) * position_size - position_size
else: # not a buy signal
    potential_profit = 0

# Calculate the Kelly Criterion fraction based on the potential profit
if potential_profit > 0:
    kelly_fraction = (win_rate * payoff_ratio - (1 - win_rate)) / payoff_ratio
else:
    kelly_fraction = 0

# Determine the position size based on the updated Kelly Criterion fraction
position_size = available_balance * kelly_fraction * risk / current_price

# Place a buy order if the prediction is 1 (buy signal) and the potential profit is positive
if prediction == 1 and potential_profit > 0:
    # order = client.order_market_buy(
    #     symbol=ticker,
    #     quantity=position_size
    # )
    print("Bought ", position_size, ticker, " at ", current_price)

# Place a sell order if the prediction is -1 (sell signal)
elif prediction == -1:
    # order = client.order_market_sell(
    #     symbol=ticker,
    #     quantity=position_size
    # )
    print("Sold ", position_size, ticker, " at ", current_price)

# Do nothing if the prediction is 0 (hold signal) or the potential profit is negative
else:
    print("Holding ", ticker)