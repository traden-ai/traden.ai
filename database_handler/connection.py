from pymongo import MongoClient

passwords = {
    "Admin": "StockTradingSim",
    "ReadOnly": "Test@123"
}


def get_client():
    username = "Admin"
    password = "StockTradingSim"
    db_name = "StockData"
    uri = "mongodb+srv://{}:{}@cluster0.em20u.mongodb.net/{}?retryWrites=true&w=majority"\
        .format(username, password, db_name)
    return MongoClient(uri)


def get_database(database):
    return get_client()[database]


def get_collection(database, collection):
    return get_database(database)[collection]
