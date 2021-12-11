'''
Class in charge of performing CRUD on Client & Contacts Collections
'''

from bson import ObjectId
from datetime import datetime, timedelta
from MongoCollection import MongoCollection
from DBDocuments import Clients, Contacts


class ClientsCollection:
    def __init__(self, database_name: str):
        self.myCol = MongoCollection(database_name, "Clients")

    def get_all(self, condition_str: {} = None):
        return self.myCol.find(condition=condition_str)

    def get_by_id(self, _id: str) -> {}:
        condition_str = {"_id": ObjectId(_id)}
        return self.myCol.find_one(condition=condition_str)

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
        return self.myCol.update_one(condition_str, {"$set": client.definition})

    def insert(self, client: Clients):
        result = self.myCol.insert(client.definition)
        return result


class ContactsCollection:
    def __init__(self, database_name: str):
        self.myCol = MongoCollection(database_name, "Contacts")

    # Get all contact records making use of the lookup function to get the project info and client info.
    # methods allows for entry of a condition to limit results
    def get_all(self, condition_str: {} = None):
        if condition_str is None:
            condition_str = {}

        join_str = [
            # phase 1 join to Client table with clientid
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
            }},
            # phase 3 join to clients projects
            {"$lookup": {
                'from': 'Projects',
                'localField': 'clientid',
                'foreignField': 'clientid',
                'as': 'projects'
            }},
            # phase 4 apply filter if needed
            {"$match": condition_str},
            # phase 5 remove projects information
            {"$project": {
                "projects":0
            }}
        ]
        return self.myCol.aggregate(join_str)

    # makes use of the openeded build of the getall and passes a condition
    def get_by_clientid(self, clientid: str) -> {}:
        condition_str = {"clientid": ObjectId(clientid)}
        return self.get_all(condition_str=condition_str)

    def get_by_id(self, _id: str) -> {}:
        condition_str = {"_id": ObjectId(_id)}
        return self.myCol.find_one(condition=condition_str)

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
