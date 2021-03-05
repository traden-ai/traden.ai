from .connection import get_client, get_database, get_collection
from .constants import DATABASE, COLLECTION
    
def insert_items(items, database= DATABASE, collection = COLLECTION):
    if isinstance(items,list):
        db = get_collection(database, collection)
        db.insert_many(item)
    else:
        db = get_collection(database, collection)
        db.insert_one(items)

def remove_item(ticker, database = DATABASE, collection = COLLECTION):
    db = get_collection(database, collection)
    db.delete_one({"Symbol": ticker})

def remove_multiple(spec, database = DATABASE, collection = COLLECTION):
    """ spec is a document with item specifications"""
    db = get_collection(database, collection)
    db.delete_many(spec)

def query_item(ticker, database = DATABASE, collection = COLLECTION):
    db = get_collection(database, collection)
    return db.find_one({"Symbol": ticker})

def get_entire_collection(database = DATABASE, collection = COLLECTION):
    db = get_collection(database, collection)
    return list(db.find({}))

def update_item(ticker, new_data, database = DATABASE, collection = COLLECTION):
    db = get_collection(database, collection)
    db.find_one_and_update({"Symbol": ticker}, {"$set": {"Data": new_data}})