#!/bin/python3
import os
import subprocess
import argparse
from pymongo import MongoClient
import datetime

def restore_database(directory, host="localhost", port=27017, exclude_databases=None):
    start_time = datetime.datetime.now()

    # Create a MongoDB client
    client = MongoClient(f'mongodb://{host}:{port}/')

    # Get the list of database names
    databases = [db_name for db_name in os.listdir(directory) if db_name not in exclude_databases]

    for db_name in databases:
        db_directory = os.path.join(directory, db_name)

        # Restore command
        restore_command = [
            "mongorestore",
            "--host", host,
            "--port", str(port),
            "--nsInclude", f"{db_name}.*",
            db_directory  # Specify the correct path to the BSON files
        ]

        # Run the restore command
        subprocess.run(restore_command)

    end_time = datetime.datetime.now()
    duration = end_time - start_time

    print("Restore completed successfully.")
    print(f"Total duration: {duration}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MongoDB Restore Script")
    parser.add_argument("directory", help="Path to the directory containing the MongoDB dump")
    parser.add_argument("--host", help="MongoDB host (default: localhost)", default="localhost")
    parser.add_argument("--port", help="MongoDB port (default: 27017)", type=int, default=27017)
    parser.add_argument("--exclude", help="Databases to exclude (comma-separated)", default="admin,local,config")

    args = parser.parse_args()

    exclude_databases = [db.strip() for db in args.exclude.split(",")]

    restore_database(args.directory, args.host, args.port, exclude_databases)
