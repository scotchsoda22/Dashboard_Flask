import pandas as pd
import sqlite3
import time
from exchanges import exchange

# Define the database filename and table name
DATABASE = "crypto.db"
TABLE_NAME = "crypto_data"

# Define the function to create the table in the database if it doesn't exist
def create_table():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (exchange TEXT, coin TEXT, bidRate FLOAT, askRate FLOAT, timestamp INTEGER)")
    conn.commit()
    conn.close()

# Define the function to insert data into the table
def insert_data(df):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    for index, row in df.iterrows():
        c.execute(f"INSERT INTO {TABLE_NAME} VALUES (?, ?, ?, ?, ?)", (row['exchange'], row['symbol'], row['bidRate'], row['askRate'], int(time.time())))
    conn.commit()
    conn.close()

# Define the function to retrieve the latest data from the table
def get_latest_data():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY timestamp DESC LIMIT 1")
    latest_data = c.fetchone()
    conn.close()
    return latest_data

# # Create the table in the database if it doesn't exist
# create_table()

# Set the interval time for data retrieval and insertion
interval = 300  # 5 minutes

while True:
    # Instantiate the exchange class and retrieve the combined DataFrame
    ex = exchange()
    df = ex.combine_dataframes()
    
    # Check if the latest data is different from the new data
    latest_data = get_latest_data()
    if latest_data is not None:
        latest_data = (latest_data[0], latest_data[1], latest_data[2], latest_data[3])
        if (df.iloc[0]['exchange'], df.iloc[0]['symbol'], df.iloc[0]['bidRate'], df.iloc[0]['askRate']) == latest_data:
            print("No new data to insert.")
            time.sleep(interval)
            continue
    
    # Insert the new data into the table
    insert_data(df)
    print("New data inserted into the database.")
    
    # Wait for the next interval
    time.sleep(interval)
