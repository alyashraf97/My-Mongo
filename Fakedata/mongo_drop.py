#!/bin/python3
from pymongo import MongoClient
import argparse
import sys

def drop_databases_except(client, databases_to_exclude):
    # Get the list of all database names
    all_databases = client.list_database_names()

    for db_name in all_databases:
        if db_name not in databases_to_exclude:
            print(f"Dropping database: {db_name}")
            client.drop_database(db_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MongoDB Database Dropper Script")
    parser.add_argument("--host", help="MongoDB host", required=True)
    parser.add_argument("--port", help="MongoDB port", type=int, required=True)

    args = parser.parse_args()

    # Databases to exclude from dropping
    databases_to_exclude = ["admin", "local", "config"]

    # Create a MongoDB client
    client = MongoClient(f'mongodb://{args.host}:{args.port}/')

    # Drop all databases except the specified ones
    drop_databases_except(client, databases_to_exclude)

    print("Databases dropped successfully.")
