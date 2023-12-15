#!/bin/python3
import os
import subprocess
from pymongo import MongoClient
import datetime as dt
import pytz

mongodb_host = "192.168.1.122"
mongodb_port = "27017"

config = {
    '_id': 'rs0', 'members':
    [
        {'_id': 0, 'host': '192.168.1.122:27017'},
        {'_id': 1, 'host': '192.168.1.123:27017'}
    ] 
}

client = MongoClient(f'mongodb://{mongodb_host}:{mongodb_port}')

client.admin.command("replSetInitiate", config)
