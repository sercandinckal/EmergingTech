from bson import ObjectId
from datetime import datetime, timedelta
from MongoCollection import MongoCollection
from DBDocuments import *


class ClientsCollection:
    def __init__(self, database_name: str):
        self.myCol = MongoCollection(database_name, "Clients")

    def get_all(self):
        return self.myCol.find()

    def get_by_id(self, _id: str) -> {}:
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.find_one(condition=condition_str)
        return result

    def get_by_clientname(self, clientname: str) -> {}:
        condition_str = {"clientname": clientname}
        result = self.myCol.find_one(condition=condition_str)
        return result

    def delete_by_id(self, _id: str):
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.delete_one(condition_str)
        return result

    def update_by_id(self, _id: str, client: Clients):
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.update_one(condition_str, {"$set": client.definition})
        return result

    def insert(self, client: Clients):
        result = self.myCol.insert(client.definition)
        return result


class ContactsCollection:
    def __init__(self, database_name: str):
        self.myCol = MongoCollection(database_name, "Contacts")

    def get_all(self, condition_str: {} = None):

        if condition_str is None:
            condition_str = {}

        join_str = [
            # phase 0 apply filter if needed
            {"$match": condition_str},
            # phase 1 connect to Client table with clientid
            {"$lookup": {
                'from': 'Clients',
                'localField': 'clientid',
                'foreignField': '_id',
                'as': 'client'
            }},
            # phase 2 will return 1 result, take it out of array
            {"$unwind": {
                "path": "$client",
                "preserveNullAndEmptyArrays": True
            }}
        ]
        return self.myCol.aggregate(join_str)

    def get_by_clientid(self, clientid: str) -> {}:
        condition_str = {"clientid": ObjectId(clientid)}
        result = self.myCol.find_one(condition=condition_str)
        return result

    def get_by_id(self, _id: str) -> {}:
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.find_one(condition=condition_str)
        return result

    def delete_by_id(self, _id: str):
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.delete_one(condition_str)
        return result

    def update_by_id(self, _id: str, contact: Contacts):
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.update_one(condition_str, {"$set": contact.definition})
        return result

    def insert(self, contact: Contacts):
        result = self.myCol.insert(contact.definition)
        return result
