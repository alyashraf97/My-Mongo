#!/bin/python3
import os
import subprocess
from pymongo import MongoClient
import datetime as dt
import pytz

# MongoDB server connection parameters
mongodb_host = "192.168.1.31"
mongodb_port = "27017"

# Set the desired timezone
desired_timezone = "Africa/Cairo"

# Create a timezone object
cairo_timezone = pytz.timezone(desired_timezone)

# The directory where the backup will be stored
current_time = dt.datetime.now(cairo_timezone)
time_format = "%Y-%m-%d_%H:%M:%S"
target_directory_name = f'MongoDump-{current_time.strftime(time_format)}'

# Create a MongoDB client
client = MongoClient(f'mongodb://{mongodb_host}:{mongodb_port}')

try:
    target_directory = os.path.join(os.getcwd(), target_directory_name)
    os.makedirs(target_directory)
    print(f"Created directory with path: {target_directory}")

    # Get the list of database names
    databases = client.list_database_names()

    for db_name in databases:
        # Create a directory for the database
        db_directory = os.path.join(target_directory, db_name)
        os.makedirs(db_directory)

        # Get the database
        db = client[db_name]
        print(f"Found DB {db_name}")

        # Get the list of collection names
        collections = db.list_collection_names()

        for collection_name in collections:
            print(f"Found collection: {collection_name}")
            # Create a directory for the collection
            collection_directory = os.path.join(db_directory, collection_name)
            os.makedirs(collection_directory)
            print(f"Backing up collection: {collection_name}")

            command = [
                "mongodump",
                "--host", mongodb_host,
                "--port", mongodb_port,
                "--db", db_name,
                "--collection", collection_name,
                "--out", collection_directory
            ]

            # Run the command
            subprocess.run(command)

finally:
    # Close the MongoDB client connection in the finally block
    client.close()
