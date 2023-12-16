#!/bin/python3
import os
import subprocess
from pymongo import MongoClient
import datetime as dt

# MongoDB server connection parameters
mongodb_host = "192.168.1.100"
mongodb_port = "27017"
# mongodb_user = 'your_username'
# mongodb_pass = 'your_password'

# The directory where the backup will be stored
timestamp = dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
backup_directory_name = f'MongoDump-{timestamp}'

# Create a MongoDB client
# client = MongoClient(f'mongodb://{mongodb_user}:{mongodb_pass}@
#       {mongodb_host}:{mongodb_port}/')
client = MongoClient(f'mongodb://{mongodb_host}:{mongodb_port}/')

backup_directory = os.path.join(os.getcwd(), backup_directory_name)
os.makedirs(backup_directory)
print(f"Created directory with path: {backup_directory}")

# Get the list of database names
databases = client.list_database_names()

for db_name in databases:
    # Create a directory for the database
    db_directory = os.path.join(backup_directory, db_name)
    os.makedirs(db_directory)
    print(f"Backing up the database: {db_directory}..")

    # Backup command
    backup_command = [
        "mongodump",
        "--host", mongodb_host,
        "--port", mongodb_port,
        "--db", db_name,
        "--out", db_directory  # Store BSON files directly in the database directory
    ]

    # Run the backup command
    subprocess.run(backup_command)

print("Backup completed successfully.")
