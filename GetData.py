# Importing necessary modules
from binance_historical_data import BinanceDataDumper
import datetime

#todays date
today = datetime.date.today()

# Creating an instance of BinanceDataDumper class
# Setting the path to the directory where dumped data will be saved,
# the type of data to be dumped (klines), and the frequency of the data (daily).
data_dumper = BinanceDataDumper(
    path_dir_where_to_dump=r"C:\Users\jonat\Documents\crypto",
    data_type="klines",
    data_frequency="1d",
)


#Data Dumper 2 for last months hourly data
data_dumper2 = BinanceDataDumper(
    path_dir_where_to_dump=r"C:\Users\jonat\Documents\crypto\spot2",
    data_type="klines",
    data_frequency="1h",
)


# Dumping historical data for SOLUSDT,
# excluding the "UST" ticker, and not updating existing data.
'''
data_dumper.dump_data(
    tickers=["SOLUSDT"],
    date_start=None,
    date_end=None,
    is_to_update_existing=False,
    tickers_to_exclude=["UST"],
)
'''

# Repeat the process for last months hourly data
'''
data_dumper2.dump_data(
    tickers=["SOLUSDT"],
    date_start=today - datetime.timedelta(days=30),
    date_end= today,
    is_to_update_existing=False,
    tickers_to_exclude=["UST"],
)
'''

# Updating existing data for this ticker.
data_dumper.dump_data(
    tickers=["SOLUSDT"],
    is_to_update_existing=True
)

# Updating existing hourly data for this ticker
data_dumper2.dump_data(
    date_start=today - datetime.timedelta(days=30),
    date_end= today,
    tickers=["SOLUSDT"],
    is_to_update_existing=True
)

# Deleting any outdated daily results that are no longer needed.
data_dumper.delete_outdated_daily_results()

#Deleting any outdated hourly results that aren't needed.
data_dumper2.delete_outdated_daily_results()