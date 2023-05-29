import sqlite3
import pandas as pd
from django.db import models

# Define the Excel file path
excel_file_path = "items.xlsx"

# Define the SQLite database file path
db_file_path = "db.sqlite3"

data_frame = pd.read_excel(excel_file_path)

# Connect to the SQLite database
connection = sqlite3.connect(db_file_path)
cursor = connection.cursor()

# Create a table in the database (if not exists)
table_name = "app_item"
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (item_name TEXT, item_packaging_type TEXT, item_detail TEXT, item_company TEXT)"
cursor.execute(create_table_query)

# Iterate over the rows in the DataFrame and insert them into the SQLite database
for _, row in data_frame.iterrows():
    item_name = row['ItemName']
    item_packaging_type = row['Pack']
    item_detail = row['ItemDetail']
    item_company = row['CompanyName']
    item_low_stock_alert = 0
    insert_query = f"INSERT INTO {table_name} (item_name, item_packaging_type, item_detail, item_company, item_low_stock_alert) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(insert_query, (item_name, item_packaging_type, item_detail, item_company, item_low_stock_alert))

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Data insertion completed.")