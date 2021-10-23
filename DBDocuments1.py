from bson import ObjectId
from datetime import datetime
from MongoCollection import MongoCollection

# connection string to mongoDB
conn_str = "mongodb+srv://sa:COLLAB_3444@cluster0.jseia.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"




class Clients:
    def __init__(self):
        self.definition = {}

    def add_client(self, _id=None, clientname: str = "", industry: str = "", description: str = "",
                   phone: str = "", email: str = "", addr1: str = "", addr2: str = "", addr3: str = "",
                   country: str = "", notes: str = ""):
        if _id is None:
            _id = ObjectId()
        self.definition = {"_id": _id, "clientname": clientname, "industry": industry, "description": description,
                           "phone": phone, "email": email, "addr1": addr1, "addr2": addr2, "addr3": addr3,
                           "country": country, "notes": notes}

    def update_client(self, _id=None, clientname: str = None, industry: str = None, description: str = None,
                   phone: str = None, email: str = None, addr1: str = None, addr2: str = None, addr3: str = None,
                   country: str = None, notes: str = None):
        if _id is not None:
            if type(_id) is str:
                self.definition["_id"] = ObjectId(_id)
            elif type(_id) is ObjectId:
                self.definition["_id"] = _id
        if clientname is not None: self.definition["clientname"] = clientname
        if industry is not None: self.definition["industry"] = industry
        if description is not None: self.definition["description"] = description
        if phone is not None: self.definition["phone"] = phone
        if email is not None: self.definition["email"] = email
        if addr1 is not None: self.definition["addr1"] = addr1
        if addr2 is not None: self.definition["addr2"] = addr2
        if addr3 is not None: self.definition["addr3"] = addr3
        if country is not None: self.definition["country"] = country
        if notes is not None: self.definition["notes"] = notes

    def add_by_json(self, client_details):
        self.definition = client_details


class ClientsCollection:
    def __init__(self, database_name: str):
        self.myCol = MongoCollection(conn_str, database_name, "Clients")

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


class Contacts:
    def __init__(self):
        self.definition = {}

    def add_contact(self, _id=None, firstname: str = "", lastname: str = "", title: str = "", role: str = "",
                    email: str = "", phone: str = "", notes: str = "", clientid: str = ""):
        if _id is None:
            _id = ObjectId()
        self.definition = {"_id": _id, "firstname": firstname, "lastname": lastname, "title": title, "role": role,
                           "email": email, "phone": phone, "notes": notes, "clientid": clientid}

    def update_contact(self, _id=None, firstname: str = None, lastname: str = None, title: str = None, role: str = None,
                    email: str = None, phone: str = None, notes: str = None, clientid: str = None):
        if _id is not None:
            if type(_id) is str:
                self.definition["_id"] = ObjectId(_id)
            elif type(_id) is ObjectId:
                self.definition["_id"] = _id
        if firstname is not None: self.definition["firstname"] = firstname
        if lastname is not None: self.definition["lastname"] = lastname
        if title is not None: self.definition["title"] = title
        if role is not None: self.definition["role"] = role
        if email is not None: self.definition["email"] = email
        if phone is not None: self.definition["phone"] = phone
        if notes is not None: self.definition["notes"] = notes
        if clientid is not None: self.definition["clientid"] = clientid

    def add_by_json(self, contact_details):
        self.definition = contact_details


class ContactsCollection:
    def __init__(self, database_name: str):
        self.myCol = MongoCollection(conn_str, database_name, "Contacts")

    def get_all(self):
        return self.myCol.find()

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

    def add_projects(self, _id=None, projectname: str = None, description: str = None, notes: str = None,
                 Status: str = None, percentcomplete: str = None, startdate: str = None, enddate: str = None,
                 clientid: str = None, projectmanagerid: str = None, projectteam: [] = None, milestones: [] = None):
        if _id is None:
            _id = {}
        self.definition = {"_id": _id, "projectname": projectname, "description": description, "notes": notes,
                           "Status": Status,"percentcomplete": percentcomplete, "startdate": startdate,
                           "enddate": enddate, "clientid": clientid, "projectmanagerid": projectmanagerid,
                           "projectteam": projectteam,"milestones": milestones}

        # add by json string from query result
    def add_by_json(self, project_details):
        self.definition = project_details

    def add_to_project_team(self, member: ProjectTeam): pass

    def modify_project_member(self, index: int, member: ProjectTeam): pass

    def delete_project_member(self, index: int): pass

    def add_to_milestone(self): pass

    def modify_milestone(self, index: int, milestone: Milestones): pass

    def delete_milestone(self, index: int): pass


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
