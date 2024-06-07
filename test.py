
import sysconfig; print(sysconfig.get_paths()["purelib"])
import pymongo
from datetime import datetime

# Configuration details for MongoDB connection
config = {
    "client": "mongodb://localhost:27017/",
    "db": "AIoT_project",
    "col": "AIoT_project"
}

# Sample data to be inserted into the collection
sample_data = {
    "name": "John",
    "age": 31,
    "email": "john@example.com",
    "timestamp": datetime.now()
}

# Establish a connection to MongoDB using the provided client information from config
client = pymongo.MongoClient(config["client"])

# Access the database specified in the config dictionary
db = client[config["db"]]

# Access the collection specified in the config dictionary
col = db[config["col"]]

# Insert the sample data into the collection
col.insert_one(sample_data)