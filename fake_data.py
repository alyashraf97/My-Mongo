#!/bin/python3
from pymongo import MongoClient
from faker import Faker
import random
import os

# Create a Faker instance
fake = Faker()

# Create a MongoDB client
client = MongoClient('mongodb://192.168.1.31:27017')

# Define the database names
db_names = ['db1', 'db2', 'db3', 'db4']

# Define the collection names
collection_names = ['collection1', 'collection2', 'collection3', 'collection4']

for db_name in db_names:
    # Get the database
    db = client[db_name]

    for collection_name in random.sample(collection_names, random.randint(2, 4)):
        # Get the collection
        collection = db[collection_name]

        # Track the current size of the data
        current_size = 0

        # Define the target size (in bytes)
        target_size = random.randint(10 * 1024 * 1024, 100 * 1024 * 1024)  # Between 10 MB and 100 MB

        while current_size < target_size:
            # Generate a document with random data
            doc = {
                'name': fake.name(),
                'address': fake.address(),
                'email': fake.email(),
                'job': fake.job(),
                'text': fake.text(max_nb_chars=200)  # Limit the size of the text field
            }

            # Insert the document into the collection
            collection.insert_one(doc)

            # Update the current size of the data
            current_size += len(str(doc))

