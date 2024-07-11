import os
from dotenv import load_dotenv

from beanie import init_beanie
import motor.motor_asyncio

from models.user import User
from models.todo import Todo

load_dotenv()

aws_password = os.getenv("AWS_DOCUMENTDB_PASSWORD")
# print(aws_password)


import pymongo
# import sys

async def test_db():

    ##Create a MongoDB client, open a connection to Amazon DocumentDB as a replica set and specify the read preference as secondary preferred
    client = pymongo.MongoClient(f"mongodb://mongoUser:{aws_password}@docdb-2024-07-11-21-40-06.cby4bosjxdhy.us-east-2.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&retryWrites=false") 

    ##Specify the database to be used
    db = client.sample_database

    ##Specify the collection to be used
    col = db.sample_collection

    ##Insert a single document
    col.insert_one({'hello':'Amazon DocumentDB'})

    ##Find the document that was previously written
    x = col.find_one({'hello':'Amazon DocumentDB'})

    ##Print the result to the screen
    print(x)

    ##Close the connection
    client.close()

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://mongoUser:{aws_password}@docdb-2024-07-11-21-40-06.cluster-cby4bosjxdhy.us-east-2.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
    )

    await init_beanie(database=client.db_name, document_models=[User, Todo])
