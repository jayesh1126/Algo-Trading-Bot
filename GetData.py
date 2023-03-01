from binance_historical_data import BinanceDataDumper
import datetime
'''
Arguments:
- path_dir_where_to_dump:
    (string) Path to folder where to dump the data
- data_type=”klines”:
    (string) data type to dump: [aggTrades, klines, trades]
-str_data_frequency:
    (string) One of [1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h]
    Frequency of price-volume data candles to get
'''

data_dumper = BinanceDataDumper(
    path_dir_where_to_dump=r"C:\Users\jayes\Documents\Algo Trading Project - Johnny",
    data_type="klines",  # aggTrades, klines, trades
    data_frequency="1d",  # argument for data_type="klines"
)

'''
Arguments:
- tickers=None:
    (list) Trading pairs for which to dump data
    if equals to None - all USDT pairs will be used
- date_start=None:
    (datetime.date) The date from which to start dump
    if equals to None - every trading pair will be dumped from the early begining (the earliest is 2017-01-01)
- date_end=True=None:
    (datetime.date) The last date for which to dump data
    if equals to None - Today’s date will be used
- is_to_update_existing=False:
    (bool) Flag if you want to update the data if it’s already exist
- tickers_to_exclude=None:
    (list) Tickers to exclude from dump
'''

# data_dumper.dump_data(
#     tickers=None,
#     date_start=None,
#     date_end=None,
#     is_to_update_existing=False,
#     tickers_to_exclude=["UST"],
# )

#data_dumper.delete_outdated_daily_results()

data_dumper.dump_data(
    tickers=["SOLUSDT"],
    is_to_update_existing=True
)