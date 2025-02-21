import sqlite3
import pandas as pd
import ssl

# Disable SSL verification (if needed)
ssl._create_default_https_context = ssl._create_unverified_context

# Load the CSV data into a Pandas DataFrame
file_path = 'https://api.slingacademy.com/v1/sample-data/files/customers.csv'
data = pd.read_csv(file_path, storage_options={'User-Agent': 'Mozilla/5.0'})

# Convert the data to a DataFrame
dataframe = pd.DataFrame(data)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('customers.db')
cursor = conn.cursor()

# Create a table in SQLite based on the dataset structure
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    gender TEXT,
    age INTEGER,
    registered TEXT,
    orders INTEGER,
    spent REAL,
    job TEXT,
    hobbies TEXT,
    is_married INTEGER
)
''')

# Insert the data from the DataFrame into the SQLite table
dataframe.to_sql('customers', conn, if_exists='replace', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data successfully inserted into SQLite database.")
