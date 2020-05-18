""""
Script to dump data from data-base to 'data.json' file
"""


import pymongo
import json


# function establish mongo connection
def mongo_connection():

    mongoclient = pymongo.MongoClient(
        "mongodb://localhost:27017/")
    mongodb = mongoclient["my_data"]
    mongocol = mongodb["movies"]
    cursor = mongocol.find()

    start_task(cursor)


# function to dump data
def start_task(cursor):
    final_data = {}
    for data in cursor:
        name = data["name"].split("(")[0]
        wiki_url = data["wiki url"]
        movie = {
            "url": wiki_url
        }
        final_data[name] = movie
    try:
        with open(".././data.json", "w") as write_file:
            json.dump(final_data, write_file)
    except Exception as e:
        print("data adding error: ", e)


if __name__ == '__main__':
    mongo_connection()
