from bson import ObjectId
from datetime import datetime, timedelta
from MongoCollection import MongoCollection
from DBDocuments import *


# collection that has specific functions to users (perform users CRUD)
class UsersCollection:
    # initialize with collection instance (mycol) that communicates with the db.
    def __init__(self, database_name: str):
        self.myCol = MongoCollection(database_name, "Users")

    # a prelim for login functionality simply check if there is record corresponding to username / password
    def validate_user(self, usercode: str, password: str) -> {}:
        condition_str = {}
        column_str = {"_id", "usercode", "firstname", "lastname", "accesstype"}
        condition_str["usercode"] = {'$regex': usercode.strip(), '$options': 'i'}
        condition_str["password"] = password
        result = self.myCol.find_one(condition=condition_str, columns=column_str)
        if result is not None:
            _id = result["_id"]
            result["_id"] = str(_id)
        return result

    # a prelim for login functionality simply check if there is record corresponding to username / password
    def validate_by_email(self, email: str, password: str) -> {}:
        condition_str = {}
        column_str = {"_id", "usercode", "firstname", "lastname", "accesstype"}
        condition_str["email"] = {'$regex': email.strip(), '$options': 'i'}
        condition_str["password"] = password
        result = self.myCol.find_one(condition=condition_str, columns=column_str)
        if result is not None:
            _id = result["_id"]
            result["_id"] = str(_id)
        return result

    # for display all on page
    def get_all(self, condition_str: {} = None):
        if condition_str is None:
            condition_str = {}
        column_str = {"_id", "firstname", "lastname", "title", "role", "email", "phone", "notes", "usercode",
                      "accesstype"}
        return self.myCol.find(columns=column_str,condition=condition_str)

    # get a record by the record id
    def get_by_id(self, _id: str) -> {}:
        column_str = {"_id", "firstname", "lastname", "title", "role", "email", "phone", "notes", "usercode",
                      "accesstype"}
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.find_one(condition=condition_str, columns=column_str)
        return result

    # for display of documents related to user_id
    def get_by_userid(self, user_id: str) -> {}:
        column_str = {"_id", "firstname", "lastname", "title", "role", "email", "phone", "notes", "usercode",
                      "accesstype"}
        condition_str = {"_id": ObjectId(user_id)}
        result = self.myCol.find_one(condition=condition_str, columns=column_str)
        return result

    # not sure if this will be needed or not
    def get_by_code(self, usercode: str) -> {}:
        column_str = {"_id", "firstname", "lastname", "title", "role", "email", "phone", "notes", "usercode",
                      "accesstype"}
        condition_str = {"usercode": usercode}
        result = self.myCol.find_one(condition=condition_str, columns=column_str)
        return result

    # check if already exist before insert (not sure if we want and upsert)
    def insert(self, user: User):
        usercode = user.definition.get("usercode")
        if usercode is None or usercode == "" or self.get_by_code(usercode) is not None:
            result = None
        else:
            result = self.myCol.insert(user.definition)
        return result

    def reset_password_by_id(self, _id: str, password: str):
        condition_str = {"_id": ObjectId(_id)}
        update_val = {"$set": {"password": password}}
        result = self.myCol.update_one(condition_str, update_val)
        return result

    # not sure if we want an upsert (merge new/insert with update). not sure if we would need the id explicitly or
    # to include in the user object
    def update_by_id(self, _id: str, user: User):
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.update_one(condition_str, {"$set": user.definition})
        return result

    # not sure if we would be deleting through other means than by id
    def delete_by_id(self, _id: str):
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.delete_one(condition_str)
        return result
