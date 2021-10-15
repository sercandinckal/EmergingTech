"""
Holds class that creates a connection to a mongoDB collection

"""
import pymongo


class MongoCollection:
    def __init__(self, conn_str: str, database_name: str, collection: str):
        self.client = pymongo.MongoClient(conn_str)
        self.db = self.client[database_name]
        self.collection = self.db[collection]

    def insert(self, new_values):
        return self.collection.insert_many(new_values)

    def find_one(self, condition=None, columns=None):
        return self.collection.find_one(condition, columns)

    def find_n(self, condition=None, columns=None, n=100):
        return self.collection.find(condition, columns).limit(n)

    def find(self, condition=None, columns=None):
        return self.collection.find(condition, columns)

    def delete_one(self, condition):
        return self.collection.delete_one(condition)

    def delete(self, condition):
        return self.collection.delete_many(condition)

    def update_one(self, condition, new_values):
        return self.collection.update_one(condition, new_values)

    def update(self, condition, new_values):
        return self.collection.update_many(condition, new_values)
