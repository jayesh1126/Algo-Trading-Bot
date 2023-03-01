import os
from binance.client import Client
import pandas as pd

# init
# api_key = 
# api_secret = 

client = Client(api_key, api_secret)

# Connecting to DEMO Binance
client.API_URL = 'https://testnet.binance.vision/api'

# get balances for all assets & some account information
print(client.get_account())

# get balance for a specific asset only (BTC)
# print("BTC")
# print(client.get_asset_balance(asset='BTC'))

# get balances for futures account
# print(client.futures_account_balance())

# get balances for margin account
# print(client.get_margin_account())

# get latest price from Binance API
btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
# print full output (dictionary)
print(btc_price)


# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

# get timestamp of earliest date data is available
timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1d')
print(timestamp)

# request historical candle (or klines) data
bars = client.get_historical_klines('BTCUSDT', '1d', timestamp, limit=1000)

# delete unwanted data - just keep date, open, high, low, close
for line in bars:
    del line[5:]
# option 4 - create a Pandas DataFrame and export to CSV
btc_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])
btc_df.set_index('date', inplace=True)
print(btc_df.head())

# export DataFrame to csv
btc_df.to_csv('btc_bars3.csv')