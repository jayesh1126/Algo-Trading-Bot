# Importing necessary modules
from binance_historical_data import BinanceDataDumper
import os
import datetime

#todays date
today = datetime.date.today()


def delete_old_files():
    # Set the directory where the files are saved
    data_dir = r'<<insert_directory_here>>'
    
    # Get the current month and last month
    today = datetime.date.today()
    current_month = today.month
    last_month = (today.replace(day=1) - datetime.timedelta(days=1)).month

    # Initialize a counter to track the number of files deleted
    num_files_deleted = 0

    # Loop through the files in the data directory
    for filename in os.listdir(data_dir):
        # Check if the file name matches the format SOLUSDT-1h-YYYY-MM
        if not filename.startswith('SOLUSDT-1h-'):
            continue
        
        try:
            # Extract the date from the file name
            file_date_str = filename.split('-')[2] + '-' + filename.split('-')[3]
            file_date = datetime.datetime.strptime(file_date_str, '%Y-%m').date()
        except (IndexError, ValueError):
            # Skip files with invalid date formats
            continue

        # Check if the file date is from the current or last month
        if file_date.month not in [current_month, last_month]:
            # Delete the file
            os.remove(os.path.join(data_dir, filename))
            print(f"Deleted file: {filename}")
            num_files_deleted += 1

    # Print the number of files deleted
    if num_files_deleted == 0:
        print("No files were deleted.")
    else:
        print(f"Deleted {num_files_deleted} files.")




# Creating an instance of BinanceDataDumper class
# Setting the path to the directory where dumped data will be saved,
# the type of data to be dumped (klines), and the frequency of the data (daily).
data_dumper = BinanceDataDumper(

    path_dir_where_to_dump=r"<<insert_directory_here>>",
    data_type="klines",
    data_frequency="1d",
)


#Data Dumper 2 for last months hourly data
data_dumper2 = BinanceDataDumper(
    path_dir_where_to_dump=r"<<insert_directory_here>>",
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
    date_start= datetime.date(datetime.utcnow() - timedelta(days=30)),
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
delete_old_files()

