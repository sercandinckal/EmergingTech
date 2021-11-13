from bson import ObjectId
from datetime import datetime, timedelta
from MongoCollection import MongoCollection
from DBDocuments import *


class TasksCollection:
    def __init__(self, database_name: str):
        self.myCol = MongoCollection(database_name, "Tasks")

    def get_by_id(self, _id: str) -> {}:
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.find_one(condition=condition_str)
        return result

    def get_dashboard(self, condition_str: {} = None):
        if condition_str is None:
            condition_str = {}
        condition_str['tasks.status'] = {'$eq': 'Active'}
        join_str = [
            {"$match": {'Status': 'Active'}},
            {'$lookup': {
                'from': 'Tasks',
                'localField': '_id',
                'foreignField': 'projectid',
                'as': 'tasks'
            }},
            {'$unwind': {
                'path': '$tasks',
                'preserveNullAndEmptyArrays': False
            }},
            {'$match': condition_str},
            {"$project": {
                'late': {
                    '$cond': [
                        {'$and': [
                            {"$lt": ['$tasks.duedate', datetime.now()]},
                            {"$gt": ['$tasks.duedate', datetime.fromisoformat("1900-01-01")]}
                        ]}, 1, 0
                    ]},
                'upcoming': {
                    '$cond': [
                        {'$and': [
                            {"$gt": ['$tasks.duedate', datetime.now()]},
                            {"$lt": ['$tasks.duedate', (datetime.now() + timedelta(days=7))]}
                        ]}, 1, 0
                    ]}
            }},
            {'$group': {
                '_id': 'null',
                'count': {'$sum': 1},
                'late': {'$sum': '$late'},
                'upcoming': {'$sum': '$upcoming'}
            }}
        ]
        return self.myCol.aggregate(join_str)

    def get_pm_dashboard(self, projectmanagerid: str):
        condition_str = {'projectmanagerid': ObjectId(projectmanagerid)}
        return self.get_dashboard(condition_str)

    def get_owner_dashboard(self, ownerid: str):
        condition_str = {'tasks.ownerid': ObjectId(ownerid)}
        return self.get_dashboard(condition_str)

    def get_all(self, status: str = "All", late_only: bool = False, condition_str: {} = None):
        if condition_str is None:
            condition_str = {}
        if late_only:
            now = datetime.now()
            condition_str["duedate"] = {"$lt": now, "$ne": datetime.fromisoformat("1900-01-01")}
        if status != "All":
            condition_str["status"] = status

        join_str = [
            # phase 0 apply filter if needed
            {"$match": condition_str},
            # phase 1 connect to user table with lookup
            {"$lookup": {
                'from': 'Users',
                'localField': 'ownerid',
                'foreignField': '_id',
                'as': 'taskowner'
            }},
            # phase 2 take it out of array
            {"$unwind": {
                "path": '$taskowner',
                "preserveNullAndEmptyArrays": True
            }},
            # phase 3 connect to project table with lookup
            {"$lookup": {
                'from': 'Projects',
                'localField': 'projectid',
                'foreignField': '_id',
                'as': 'project'
            }},
            # phase 4 take it out of array
            {"$unwind": {
                "path": '$project',
                "preserveNullAndEmptyArrays": True
            }},
            # phase 5 connect to contacts table with lookup
            {"$lookup": {
                'from': 'Contacts',
                'localField': 'contactid',
                'foreignField': '_id',
                'as': 'contact'
            }},
            # phase 6 take single it out of array
            {"$unwind": {
                "path": '$contact',
                "preserveNullAndEmptyArrays": True
            }},
            # phase 7 take multi milestones it out of array
            {"$unwind": {
                "path": '$project.milestones',
                "preserveNullAndEmptyArrays": True
            }},
            # phase 8 filter multi milestones to reflect the one we are looking for
            {"$match": {
                "$or": [
                  {"$expr": {"$eq": ['$milestoneid', None]}},
                  {"$expr": {"$eq": ['$milestoneid', {}]}},
                  {"$expr": {"$eq": ['$project.milestones.milestoneid', '$milestoneid']}}
                ]
            }},
            # phase 9 & 10 extract projectname, ownername, milestonename & drop rest of the project, taskowner.
            {"$addFields": {
                'projectname': '$project.projectname',
                'ownername':{ '$concat': ['$taskowner.firstname',' ','$taskowner.lastname']},
                'contactname':{ '$concat': ['$contact.firstname',' ','$contact.lastname']},
                'milestonename': '$project.milestones.milestonename'
            }},
            {"$project": {
                'project': 0,
                'taskowner': 0
            }}
        ]
        return self.myCol.aggregate(join_str)

    def get_by_task_owner(self, ownerid: str, status: str = "All", late_only: bool = False):
        return self.get_all(status=status, late_only=late_only, condition_str={"ownerid": ObjectId(ownerid)})

    def get_by_milestone(self, milestoneid, status: str = "All", late_only: bool = False):
        return self.get_all(status=status, late_only=late_only, condition_str={"milestoneid": ObjectId(milestoneid)})

    def get_by_project(self, projectid, status: str = "All", late_only: bool = False):
        return self.get_all(status=status, late_only=late_only, condition_str={"projectid": ObjectId(projectid)})

    def get_by_contract(self, contactid, status: str = "All", late_only: bool = False):
        return self.get_all(status=status, late_only=late_only, condition_str={"contactid": ObjectId(contactid)})

    def delete_by_id(self, _id: str):
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.delete_one(condition_str)
        return result

    def update_by_id(self, _id: str, task: Tasks):
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.update_one(condition_str, {"$set": task.definition})
        return result

    def insert(self, task: Tasks):
        result = self.myCol.insert(task.definition)
        return result
