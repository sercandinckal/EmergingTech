from MongoCollection import MongoCollection


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
