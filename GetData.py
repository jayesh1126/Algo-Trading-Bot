# Importing necessary modules
from binance_historical_data import BinanceDataDumper
import datetime

# Creating an instance of BinanceDataDumper class
# Setting the path to the directory where dumped data will be saved,
# the type of data to be dumped (klines), and the frequency of the data (daily).
data_dumper = BinanceDataDumper(
    path_dir_where_to_dump=r"C:\Users\jayes\Documents\Algo Trading Project - Johnny",
    data_type="klines",
    data_frequency="1d",
)

# Dumping historical data for all available tickers and dates,
# excluding the "UST" ticker, and not updating existing data.
'''
data_dumper.dump_data(
    tickers=None,
    date_start=None,
    date_end=None,
    is_to_update_existing=False,
    tickers_to_exclude=["UST"],
)
'''

# Dumping historical data for a specific ticker ("SOLUSDT")
# and updating existing data for this ticker.
data_dumper.dump_data(
    tickers=["SOLUSDT"],
    is_to_update_existing=True
)

# Deleting any outdated daily results that are no longer needed.
data_dumper.delete_outdated_daily_results()