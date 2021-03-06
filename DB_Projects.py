'''
Class in charge of performing CRUD on Project, project team & project milestone objects.
All were stored in the Project collection to make use of the mongoDB schemaless capabilities
'''
from bson import ObjectId
from datetime import datetime, timedelta
from MongoCollection import MongoCollection
from DBDocuments import *


class ProjectsCollection:
    def __init__(self, database_name: str):
        self.myCol = MongoCollection(database_name, "Projects")

    # get project dashboard by project manager
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

    # get all projects when no parameter is entered
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
            }},
            # phase 5 remove passwordfield
            {"$project": {
                "projectmanager.password":0
            }}
        ]
        return self.myCol.aggregate(join_str)

    def get_by_id(self, _id: str) -> {}:
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.find_one(condition=condition_str)
        return result

    # Make use of the dynamic get all to get projects by its manager
    def get_by_prj_manager(self, user_id: str, status: str = "All", late_only: bool = False):
        condition_str = {"projectmanagerid": ObjectId(user_id)}
        return self.get_all(status=status, late_only=late_only, condition_str=condition_str)

    # get project where the user_id is on the project team
    def get_by_prj_member(self, user_id: str, status: str = "All", late_only: bool = False):
        condition_str = {"projectteam.prjteamid":ObjectId(user_id)}
        return self.get_all(status=status, late_only=late_only, condition_str=condition_str)

    # get projects by clientid
    def get_by_client(self, clientid: str, status: str = "All", late_only: bool = False):
        condition_str = {"clientid": ObjectId(clientid)}
        return self.get_all(status=status, late_only=late_only, condition_str=condition_str)

    # get projectas by milestoneid
    def get_by_milestoneid(self, milestoneid: str, status: str = "All", late_only: bool = False):
        condition_str = {"milestones.milestoneid": ObjectId(milestoneid)}
        return self.get_all(status=status, late_only=late_only, condition_str=condition_str)

    def get_by_projectname(self, projectname:str, status: str = "All", late_only: bool = False):
        condition_str = {"projectname": projectname}
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

    # get all the milstones, had to breakup project objects to extract
    def get_all_milestones(self, condition_str: {} = None):
        if condition_str is None:
            condition_str = {}

        join_str = [
            # phase 0 breakup milestone array
            {"$unwind": {
                "path": "$milestones",
                "includeArrayIndex": "milestonesidx",
                "preserveNullAndEmptyArrays": False
            }},
            # phase 1 apply filter if needed
            {"$match": condition_str},
            # phase 2 Select related columns and put in presentable format.
            {"$project": {
                "_id": "$milestones.milestoneid",
                "milestoneid": "$milestones.milestoneid",
                "projectid": "$_id",
                "milestonesidx": "$milestonesidx",
                "projectname": "$projectname",
                "milestonename": "$milestones.milestonename",
                "duedate": "$milestones.duedate",
                "status": "$milestones.status",
                "description": "$milestones.description"
            }}
        ]
        return self.myCol.aggregate(join_str)

    # uses the get all milestones method
    def get_milestones_by_projectid(self, projectid: str):
        condition_str = {"_id": ObjectId(projectid)}
        return self.get_all_milestones(condition_str=condition_str)

    # uses the get all milestones method
    def get_milestones_by_milestoneid(self, milestoneid: str):
        condition_str = {"milestones.milestoneid": ObjectId(milestoneid)}
        return self.get_all_milestones(condition_str=condition_str)

    # due to it being an array in project need to know which project to add it to
    def insert_milestones(self, projectid: str, milestone: Milestones):
        condition_str = {"_id": ObjectId(projectid)}
        return self.myCol.update_one(condition_str, {"$addToSet": {'milestones':milestone.definition}})

    # due to it being an array in project need to know which project to modify
    def update_milestones_by_idx(self, projectid: str, idx: int, milestone: Milestones):
        condition_str = {"_id": ObjectId(projectid)}
        return self.myCol.update_one(condition_str, {"$set": {'milestones'+str(idx)+'.content': milestone.definition}})

    def delete_milestones(self, projectid: str, milestoneid: int):
        condition_str = {"_id": ObjectId(projectid)}
        return self.myCol.update_one(condition_str, {"$pull": {"milestones": {"milestoneid": ObjectId(milestoneid)}}})

    # get all the project team members, had to breakup project objects to extract
    def get_all_prjteam(self, condition_str: {} = None):
        if condition_str is None:
            condition_str = {}

        join_str = [
            # phase 1 breakup array
            {"$unwind": {
                "path": "$projectteam",
                "includeArrayIndex": "prjtteamidx",
                "preserveNullAndEmptyArrays": False
            }},
            # phase 1 apply filter if needed
            {"$match": condition_str},
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
                "role": "$projectteam.role",
                "firstname": "$projectteam.team.firstname",
                "lastname": "$projectteam.team.lastname"
            }}
        ]
        return self.myCol.aggregate(join_str)

    # used the get_all method passing the projectid as a filter
    def get_prjteam_by_projectid(self, projectid: str):
        condition_str = {"_id": ObjectId(projectid)}
        return self.get_all_prjteam(condition_str=condition_str)

    # used the get_all method passing the user id as a filter
    def get_prjteam_by_prjteamid(self, prjteamid: str):
        condition_str = {"projectteam.prjteamid": ObjectId(prjteamid)}
        return self.get_all_prjteam(condition_str=condition_str)

    def insert_prjteam(self, projectid: str, prjteam: ProjectTeam):
        condition_str = {"_id": ObjectId(projectid)}
        return self.myCol.update_one(condition_str, {"$addToSet": {'projectteam': prjteam.definition}})

    def update_prjteam_by_idx(self, projectid: str, idx: int, prjteam: ProjectTeam):
        condition_str = {"_id": ObjectId(projectid)}
        return self.myCol.update_one(condition_str, {"$set": {'projectteam'+str(idx)+'.content': prjteam.definition}})

    def delete_prjteam(self, projectid: str, prjteamid: str):
        condition_str = {"_id": ObjectId(projectid)}
        return self.myCol.update_one(condition_str, {"$pull": {"projectteam": {"prjteamid": ObjectId(prjteamid)}}})
