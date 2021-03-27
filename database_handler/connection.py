from pymongo import MongoClient


def get_client():
    password = "StockTradingSim"
    db_name = "StockData"
    uri = "mongodb+srv://Admin:{}@cluster0.em20u.mongodb.net/{}?retryWrites=true&w=majority".format(password, db_name)
    return MongoClient(uri)


def get_database(database):
    return get_client()[database]


def get_collection(database, collection):
    return get_database(database)[collection]
