from bson import ObjectId
from datetime import datetime, timedelta
from MongoCollection import MongoCollection
from DBDocuments import *


class ProjectsCollection:
    def __init__(self, database_name: str):
        self.myCol = MongoCollection(database_name, "Projects")

    def get_my_dashboard(self, projectmanagerid: str):
        condition_str = {'Status': 'Active', 'projectmanagerid': ObjectId(projectmanagerid)}
        join_str = [
            {"$match": condition_str},
            {"$project": {
                'late': {
                    '$cond': [
                        {'$and': [
                            {"$lt": ['$enddate', datetime.now()]},
                            {"$gt": ['$enddate', datetime.fromisoformat("1900-01-01")]}
                        ]}, 1, 0
                    ]}
            }},
            {'$group':{
            '_id': 'null',
            'count': {'$sum': 1},
            'late': {'$sum': '$late'}
            }}
        ]
        return self.myCol.aggregate(join_str)

    def get_all(self, status: str = "All", late_only: bool = False, condition_str: {} = None):
        if condition_str is None:
            condition_str = {}

        if late_only:
            now = datetime.now()
            condition_str["enddate"] = {"$lt": now, "$ne": datetime.fromisoformat("1900-01-01")}
        if status != "All":
            condition_str["Status"] = status

        join_str = [
            # phase 0 apply filter if needed
            {"$match": condition_str},
            # phase 1 connect to user table with project manager
            {"$lookup": {
                'from': 'Users',
                'localField': 'projectmanagerid',
                'foreignField': '_id',
                'as': 'projectmanager'
            }},
            # phase 2 will return 1 result, take it out of array
            {"$unwind": {
                "path": "$projectmanager",
                "preserveNullAndEmptyArrays": True
            }},
            # phase 3 connect to Client table with clientid
            {"$lookup": {
                'from': 'Clients',
                'localField': 'clientid',
                'foreignField': '_id',
                'as': 'client'
            }},
            # phase 4 will return 1 result, take it out of array
            {"$unwind": {
                "path": "$client",
                "preserveNullAndEmptyArrays": True
            }}
        ]
        return self.myCol.aggregate(join_str)

    def get_by_id(self, _id: str) -> {}:
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.find_one(condition=condition_str)
        return result

    def get_by_prj_manager(self, user_id: str, status: str = "All", late_only: bool = False):
        condition_str = {"projectmanagerid": ObjectId(user_id)}
        return self.get_all(status=status, late_only=late_only, condition_str=condition_str)

    def get_by_prj_member(self, user_id: str, status: str = "All", late_only: bool = False):
        condition_str = {"projectteam.prjteamid":ObjectId(user_id)}
        return self.get_all(status=status, late_only=late_only, condition_str=condition_str)

    def get_by_client(self, clientid: str, status: str = "All", late_only: bool = False):
        condition_str = {"clientid": ObjectId(clientid)}
        return self.get_all(status=status, late_only=late_only, condition_str=condition_str)

    def get_by_milestoneid(self, milestoneid: str, status: str = "All", late_only: bool = False):
        condition_str = {"milestones.milestoneid": ObjectId(milestoneid)}
        return self.get_all(status=status, late_only=late_only, condition_str=condition_str)

    def delete_by_id(self, _id: str):
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.delete_one(condition_str)
        return result

    def update_by_id(self, _id: str, project: Projects):
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.update_one(condition_str, {"$set": project.definition})
        return result

    def insert(self, project: Projects):
        result = self.myCol.insert(project.definition)
        return result

    def get_all_milestones(self, condition_str: {} = None):
        if condition_str is None:
            condition_str = {}

        join_str = [
            # phase 0 apply filter if needed
            {"$match": condition_str},
            # phase 1 breakup array
            {"$unwind": {
                "path": "$milestones",
                "includeArrayIndex": "milestonesidx",
                "preserveNullAndEmptyArrays": True
            }},
            # phase 2 Select related columns and put in presentable format.
            {"$project": {
                "_id": "$milestones.milestoneid",
                "milestoneid": "$milestones.milestoneid",
                "projectid": "$_id",
                "projectname": "$projectname",
                "milestonename": "$milestones.milestonename",
                "duedate": "$milestones.duedate",
                "status": "$milestones.status",
                "description": "$milestones.description"
            }}
        ]
        return self.myCol.aggregate(join_str)

    def get_milestones_by_projectid(self, projectid: str):
        condition_str = {"_id": ObjectId(projectid)}
        return self.get_all_milestones(condition_str=condition_str)

    def get_milestones_by_milestoneid(self, milestoneid: str):
        condition_str = {"milestones.milestoneid": ObjectId(milestoneid)}
        return self.get_all_milestones(condition_str=condition_str)

    def get_all_prjteam(self, condition_str: {} = None):
        if condition_str is None:
            condition_str = {}

        join_str = [
            # phase 0 apply filter if needed
            {"$match": condition_str},
            # phase 1 breakup array
            {"$unwind": {
                "path": "$projectteam",
                "includeArrayIndex": "prjtteamidx",
                "preserveNullAndEmptyArrays": True
            }},
            # phase 2 connect to user table with lookup
            {"$lookup": {
                "from": "Users",
                "localField": "projectteam.prjteamid",
                "foreignField": "_id",
                "as": "projectteam.team"
            }},
            # phase 3 will return 1 result, take it out of array
            {"$unwind": {
                "path": "$projectteam.team",
                "preserveNullAndEmptyArrays": True
            }},
            # phase 4 rename columns and put in presentable format.
            {"$project": {
                "_id": "$projectteam.prjteamid",
                "prjteamid": "$projectteam.prjteamid",
                "projectid": "$_id",
                "projectname": "$projectname",
                "prjtteamidx": 1,
                "roles": "$projectteam.role",
                "firstname": "$projectteam.team.firstname",
                "lastname": "$projectteam.team.lastname"
            }}
        ]
        return self.myCol.aggregate(join_str)

    def get_prjteam_by_projectid(self, projectid: str):
        condition_str = {"_id": ObjectId(projectid)}
        return self.get_all_prjteam(condition_str=condition_str)

    def get_prjteam_by_prjteamid(self, prjteamid: str):
        condition_str = {"projectteam.prjteamid": ObjectId(prjteamid)}
        return self.get_all_prjteam(condition_str=condition_str)
