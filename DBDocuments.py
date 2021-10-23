from bson import ObjectId
from datetime import datetime
from MongoCollection import MongoCollection

# connection string to mongoDB
conn_str = "mongodb+srv://sa:COLLAB_3444@cluster0.jseia.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

class Clients:
    def __init__(self):
        self.definition = {}

    def add_client(self, _id = None, clientname: str = None, industry: str = None, description: str = None,
                   phone: str = None,  email: str = None, addr1: str = None, addr2: str = None, addr3: str = None,
                   country: str = None, notes: str = None):
        if _id is None:
            _id = {}
        self.definition = {"_id": _id, "clientname": clientname, "industry": industry, "description": description,
                           "phone": phone, "email": email, "addr1": addr1, "addr2": addr2, "addr3": addr3,
                           "country": country, "notes": notes}

    def add_by_json(self, client_details):
        self.definition = client_details


class ClientsCollection:
    def __init__(self, conn_str: str, database_name: str):
        self.myCol = MongoCollection(conn_str, database_name, "Clients")

    def get_all(self):
        return self.myCol.find()

    def get_by_id(self, _id: str) -> {}:
        condition_str = {"_id": {"$oid": id}}
        result = self.myCol.find_one(condition=condition_str)
        return result

    def delete_by_id(self, _id: str): pass

    def update_by_id(self, _id: str, clients: Clients): pass

    def insert(self, clients: Clients): pass


class Contacts:
    def __init__(self):
        self.definition = {}

    def add_contact(self, _id=None, firstname: str = None, lastname: str = None, title: str = None, role: str = None,
                 email: str = None, phone: str = None, notes: str = None, clientid: str = None):
        if _id is None:
            _id = {}
        self.definition = {"_id": _id, "firstname": firstname, "lastname": lastname, "title": title, "role": role,
                           "email": email, "phone": phone, "notes": notes, "clientid": clientid}

    def add_by_json(self, contact_details):
        self.definition = contact_details


class ContactsCollection:
    def __init__(self, conn_str: str, database_name: str):
        self.myCol = MongoCollection(conn_str, database_name, "Contacts")

    def get_all(self):
        return self.myCol.find()

    def get_by_id(self, _id: str) -> {}:
        condition_str = {"_id": {"$oid": id}}
        result = self.myCol.find_one(condition=condition_str)
        return result

    def delete_by_id(self, _id: str): pass

    def update_by_id(self, _id: str, contacts: Contacts): pass

    def insert(self, contacts: Contacts): pass



class ProjectTeam:
    def __init__(self):
        self.definition = {}

        # DBA
        # front end developer
        # back end developer

    def add_projectTeam(self, _id=None, role:str = None):
        if _id is None:
            _id = {}
        self.definition = {"_id": _id, "role": role}

    def add_by_json(self, details):
        self.definition = details


class Milestones:
    def __init__(self):
        self.definition = {}

    def add_milestone(self, _id = None, milestonename: str = None, duedate: str = None, status: str = None):
        if _id is None:
            _id = {}
        self.definition = {"duedate": duedate, "milestonename": milestonename, "status": status}

    def add_by_json(self, details):
        self.definition = details



class Projects:
    def __init__(self):
        self.definition = {}

    def add_projects(self, _id=None, projectname: str = "", description: str = "", notes: str = "",
                     Status: str = "", percentcomplete: str = "", startdate: str = "", enddate: str = "",
                     clientid: str = "", projectmanagerid: str = "", projectteam: [] = None, milestones: [] = None):
        if _id is None: _id = ObjectId()
        if milestones is None: milestones = []
        if projectteam is None: projectteam = []
        self.definition = {"_id": _id, "projectname": projectname, "description": description, "notes": notes,
                           "Status": Status, "percentcomplete": percentcomplete, "startdate": startdate,
                           "enddate": enddate, "clientid": clientid, "projectmanagerid": projectmanagerid,
                           "projectteam": projectteam, "milestones": milestones}

    def update_projects(self, _id=None, projectname: str = None, description: str = None, notes: str = None,
                     Status: str = None, percentcomplete: str = None, startdate: str = None, enddate: str = None,
                     clientid: str = None, projectmanagerid: str = None, projectteam: [] = None, milestones: [] = None):
        if _id is not None:
            if type(_id) is str:
                self.definition["_id"] = ObjectId(_id)
            elif type(_id) is ObjectId:
                self.definition["_id"] = _id
        if projectname is not None: self.definition["projectname"] = projectname
        if description is not None: self.definition["description"] = description
        if notes is not None: self.definition["notes"] = notes
        if Status is not None: self.definition["Status"] = Status
        if percentcomplete is not None: self.definition["percentcomplete"] = percentcomplete
        if startdate is not None: self.definition["startdate"] = startdate
        if enddate is not None: self.definition["enddate"] = enddate
        if clientid is not None: self.definition["clientid"] = clientid
        if projectmanagerid is not None: self.definition["projectmanagerid"] = projectmanagerid
        if projectteam is not None: self.definition["projectteam"] = projectteam
        if milestones is not None: self.definition["milestones"] = milestones

    def add_by_json(self, project_details): self.definition = project_details

    def add_to_project_team(self, member: ProjectTeam): self.definition["projectteam"].append(member)

    def modify_project_member(self, index: int, member: ProjectTeam): self.definition["projectteam"][index] = member

    def get_project_team(self): return self.definition["projectteam"]

    def add_to_milestone(self, milestone: Milestones): self.definition["milestones"].append(milestone)

    def modify_milestone(self, index: int, milestone: Milestones): self.definition["milestones"][index] = milestone

    def get_milestones(self): return self.definition["milestones"]


class ProjectsCollection:
    def __init__(self, database_name: str):
        self.myCol = MongoCollection(conn_str, database_name, "Projects")

    def get_all(self, status: str = "All", late_only: bool = False):
        condition_str = {}
        if late_only:
            now = datetime.now()
            condition_str["enddate"] = {"$lt": now, "$ne": datetime.fromisoformat("1900-01-01")}
        if status != "All":
            condition_str["Status"] = status
        return self.myCol.find(condition=condition_str)

    def get_by_id(self, _id: str) -> {}:
        condition_str = {"_id": ObjectId(_id)}
        result = self.myCol.find_one(condition=condition_str)
        return result

    def get_by_prj_manager(self, user_id: str, status: str = "All", late_only: bool = False):
        condition_str = {}
        if late_only:
            now = datetime.now()
            condition_str["enddate"] = {"$lt": now, "$ne": datetime.fromisoformat("1900-01-01")}
        if status != "All":
            condition_str["Status"] = status
        condition_str["projectmanagerid"] = ObjectId(user_id)
        return self.myCol.find(condition=condition_str)

    def get_by_prj_member(self, user_id: str, status: str = "All", late_only: bool = False):
        condition_str = {}
        if late_only:
            now = datetime.now()
            condition_str["enddate"] = {"$lt": now, "$ne": datetime.fromisoformat("1900-01-01")}
        if status != "All":
            condition_str["Status"] = status
        condition_str["projectteam.prjteamid"] = ObjectId(user_id)
        return self.myCol.find(condition=condition_str)

    def get_by_client(self, clientid: str, status: str = "All", late_only: bool = False):
        condition_str = {}
        if late_only:
            now = datetime.now()
            condition_str["enddate"] = {"$lt": now, "$ne": datetime.fromisoformat("1900-01-01")}
        if status != "All":
            condition_str["Status"] = status
        condition_str["clientid"] = ObjectId(clientid)
        return self.myCol.find(condition=condition_str)

    def get_by_milestoneid(self, milestoneid: str, status: str = "All", late_only: bool = False):
        condition_str = {}
        if late_only:
            now = datetime.now()
            condition_str["enddate"] = {"$lt": now, "$ne": datetime.fromisoformat("1900-01-01")}
        if status != "All":
            condition_str["Status"] = status
        condition_str["milestones.milestoneid"] = ObjectId(milestoneid)
        return self.myCol.find(condition=condition_str)

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

    def get_milestones(self, projectid: str ): pass

    def get_all_prjteam(self, condition_str: {}= None):
        # https://stackoverflow.com/questions/2350495/how-do-i-perform-the-sql-join-equivalent-in-mongodb
        # https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/
        # https://sqlserverguides.com/mongodb-join-two-collections/

        if condition_str == None:
            condition_str = {}

        join_str = [
            # phase 0 apply filter if needed
            {"$match": condition_str},
            # phase 1 breakup array
            {"$unwind":{
                "path": "$projectteam",
                "includeArrayIndex":"prjtteamidx",
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
                "projectid": "$_id",
                "prjtteamidx": 1,
                "roles": "$projectteam.role",
                "prjteamid": "$projectteam.prjteamid",
                "firstname":"$projectteam.team.firstname",
                "lastname":"$projectteam.team.lastname"
            }}
        ]
        result = self.myCol.aggregate(join_str)
        return result

    def get_prjteam_by_projectid(self, projectid: str):
        condition_str = {"_id": ObjectId(projectid)}
        return self.get_all_prjteam(condition_str= condition_str)

    def get_prjteam_by_prjteamid(self, prjteamid: str):
        condition_str = {"projectteam.prjteamid": ObjectId(prjteamid)}
        return self.get_all_prjteam(condition_str= condition_str)




class ProjectsCollection:
    def __init__(self, conn_str: str, database_name: str):
        self.myCol = MongoCollection(conn_str, database_name, "Projects")

    def get_all(self):
        return self.myCol.find()

    def get_by_id(self, _id: str) -> {}:
        condition_str = {"_id": {"$oid": id}}
        result = self.myCol.find_one(condition=condition_str)
        return result

    def get_by_prj_manager(self, user_id): pass

    def get_by_prj_member(self, user_id): pass

    def get_milestones(self): pass

    def get_projectteam(self): pass

    def delete_by_id(self, _id: str): pass

    def update_by_id(self, _id: str, projects: Projects): pass

    def insert(self, projects: Projects): pass


class Tasks:
    def __init__(self):
        self.definition = {}

    def add_tasks(self, _id=None, taskname: str = None, description: str = None, notes: str = None,
                 status: str = None, percentagecomplete: str = None, startdate: str = None, duedate: str = None,
                 completedate: str = None, contactid: str = None,ownerid: str = None, milestoneid: str = None):
        if _id is None:
            _id = {}
        self.definition = {"_id": _id, "taskname": taskname, "description": description, "notes": notes,
                           "status": status,"percentagecomplete": percentagecomplete, "startdate": startdate,
                           "duedate": duedate, "completedate": completedate, "contactid": contactid,
                           "ownerid": ownerid,"milestoneid": milestoneid}

        # add by json string from query result
    def add_by_json(self, tasks_details):
        self.definition = tasks_details


class TasksCollection:
    def __init__(self, conn_str: str, database_name: str):
        self.myCol = MongoCollection(conn_str, database_name, "Tasks")

    def get_all(self):
        return self.myCol.find()

    def get_by_id(self, _id: str) -> {}:
        condition_str = {"_id" : {"$oid": id}}
        result = self.myCol.find_one(condition=condition_str)
        return result

    def get_by_task_owner(self, user_id): pass

    def delete_by_id(self, _id: str): pass

    def update_by_id(self, _id: str, tasks: Tasks): pass

    def insert(self, tasks: Tasks): pass


# class for a single instance user object. **Will be useful for insert & updates
class User:
    def __init__(self):
        self.definition = {}

    # create user from scratch (maybe for new???)
    def add_user(self, _id=None, firstname: str = None, lastname: str = None, title: str = None, role: str = None,
                 email: str = None, phone: str = None, notes: str = None, usercode: str = None, password: str = None,
                 accesstype: str = None):
        if _id is None:
            _id = {}
        self.definition ={"_id": _id,"firstname": firstname, "lastname": lastname, "title": title, "role": role,
                          "email": email, "phone": phone, "notes": notes, "usercode": usercode, "password": password,
                           "accesstype": accesstype}

    # add by json string from query result
    def add_by_json(self, user_details):
        self.definition = user_details


# collection that has specific functions to users (perform users CRUD)
class UsersCollection:
    # initialize with collection instance (mycol) that communicates with the db.
    def __init__(self, conn_str: str, database_name: str):
        self.myCol = MongoCollection(conn_str, database_name, "Users")

    # a prelim for login functionality simply check if there is record corresponding to username / password
    def validate_user(self, usercode: str, password: str) -> {}:
        condition_str = {}
        column_str = {"_id", "usercode", "firstname", "lastname","accesstype"}
        condition_str["usercode"] = usercode
        condition_str["password"] = password
        result = self.myCol.find_one(condition=condition_str, columns=column_str)
        if result is not None:
            _id = result["_id"]
            result["_id"] = str(_id)
        return result

    # for display all on page
    def get_all(self):
        return self.myCol.find()

    # get a record by the record id
    def get_by_id(self, _id: str) -> {}:
        condition_str = {"_id" : {"$oid": id}}
        result = self.myCol.find_one(condition=condition_str)
        return result

    # for display of documents related to user_id
    def get_by_userid(self, user_id: str): pass

    # not sure if this will be needed or not
    def get_by_code(self, usercode: str): pass

    # check if already exist before insert (not sure if we want and upsert)
    def insert(self, user: User): pass

    # not sure if we want an upsert (merge new/insert with update). not sure if we would need the id explicitly or
    # to include in the user object
    def update_by_id(self, _id: str, user: User): pass

    # not sure if we would be deleting through other means than by id
    def delete_by_id(self, _id: str): pass
