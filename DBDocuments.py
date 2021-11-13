from bson import ObjectId
from datetime import datetime, timedelta
from MongoCollection import MongoCollection


class User:
    def __init__(self):
        self.definition = {}

    # create user from scratch (maybe for new???)
    def add_user(self, _id=None, firstname: str = "", lastname: str = "", title: str = "", role: str = "",
                 email: str = "", phone: str = "", notes: str = "", usercode: str = "", password: str = "",
                 accesstype: str = ""):
        if _id is None:
            _id = ObjectId()
        self.definition = {"_id": _id, "firstname": firstname, "lastname": lastname, "title": title, "role": role,
                           "email": email, "phone": phone, "notes": notes, "usercode": usercode, "password": password,
                           "accesstype": accesstype}

    def update_user(self, _id=None, firstname: str = None, lastname: str = None, title: str = None, role: str = None,
                    email: str = None, phone: str = None, notes: str = None, usercode: str = None, password: str = None,
                    accesstype: str = None):
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
        if usercode is not None: self.definition["usercode"] = usercode
        if password is not None: self.definition["password"] = password
        if accesstype is not None: self.definition["accesstype"] = accesstype

    # add by json string from query result
    def add_by_json(self, user_details):
        self.definition = user_details


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


class ProjectTeam:
    def __init__(self):
        self.definition = {}

        # DBA
        # front end developer
        # back end developer

    def add_projectTeam(self, prjteamid=None, role: str = ""):
        if prjteamid is None:
            prjteamid = ObjectId()
        self.definition = {"prjteamid": prjteamid, "role": role}

    def update_projectTeam(self, prjteamid=None, role: str = None):
        if prjteamid is not None:
            if type(prjteamid) is str:
                self.definition["prjteamid"] = ObjectId(prjteamid)
            elif type(prjteamid) is ObjectId:
                self.definition["prjteamid"] = prjteamid
        if role is not None: self.definition["role"] = role

    def add_by_json(self, details):
        self.definition = details


class Milestones:
    def __init__(self):
        self.definition = {}

    def add_milestone(self, milestoneid=None, milestonename: str = "", duedate: str = "", status: str = ""):
        if milestoneid is None:
            milestoneid = ObjectId()
        self.definition = {"milestoneid": milestoneid, "milestonename": milestonename, "duedate": duedate,
                           "status": status}

    def update_milestone(self, milestoneid=None, milestonename: str = None, duedate: str = None, status: str = None):
        if milestoneid is not None:
            if type(milestoneid) is str:
                self.definition["milestoneid"] = ObjectId(milestoneid)
            elif type(milestoneid) is ObjectId:
                self.definition["milestoneid"] = milestoneid
        if milestonename is not None: self.definition["milestonename"] = milestonename
        if duedate is not None: self.definition["duedate"] = duedate
        if status is not None: self.definition["status"] = status

    def add_by_json(self, details):
        self.definition = details


class Projects:
    def __init__(self):
        self.definition = {}

    def add_projects(self, _id=None, projectname: str = "", description: str = "", notes: str = "", Status: str = "",
                     percentcomplete: str = "", startdate: str = "", enddate: str = "", clientid: str = "",
                     projectmanagerid: str = "", projectteam: [] = None, milestones: [] = None,
                     projectmanager: User = None, client: Clients = None):
        if _id is None: _id = ObjectId()
        if milestones is None: milestones = []
        if projectteam is None: projectteam = []
        self.definition = {"_id": _id, "projectname": projectname, "description": description, "notes": notes,
                           "Status": Status, "percentcomplete": percentcomplete, "startdate": startdate,
                           "enddate": enddate, "clientid": clientid, "projectmanagerid": projectmanagerid,
                           "projectteam": projectteam, "milestones": milestones, "projectmanager": projectmanager,
                           "client": client}

    def update_projects(self, _id=None, projectname: str = None, description: str = None, notes: str = None,
                        Status: str = None, percentcomplete: str = None, startdate: str = None, enddate: str = None,
                        clientid: str = None, projectmanagerid: str = None, projectteam: [] = None,
                        milestones: [] = None,
                        projectmanager: User = None, client: Clients = None):
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
        if projectmanager is not None: self.definition["projectmanager"] = projectmanager
        if client is not None: self.definition["client"] = client

    def add_by_json(self, project_details):
        self.definition = project_details

    def add_to_project_team(self, member: ProjectTeam):
        self.definition["projectteam"].append(member)

    def modify_project_member(self, index: int, member: ProjectTeam):
        self.definition["projectteam"][index] = member

    def get_project_team(self):
        return self.definition["projectteam"]

    def add_to_milestone(self, milestone: Milestones):
        self.definition["milestones"].append(milestone)

    def modify_milestone(self, index: int, milestone: Milestones):
        self.definition["milestones"][index] = milestone

    def get_milestones(self):
        return self.definition["milestones"]


class Tasks:
    def __init__(self):
        self.definition = {}

    def add_tasks(self, _id=None, taskname: str = "", description: str = "", notes: str = "", status: str = "",
                  percentagecomplete: str = "", startdate: str = "", duedate: str = "", completedate: str = "",
                  contactid: ObjectId = None, ownerid: ObjectId = None, milestoneid: ObjectId = None,
                  projectid: ObjectId = None, contact:Contacts = None, ownername:str = "", milestonename:str = "",
                  projectname:str = ""):
        if _id is None:
            _id = ObjectId()
        self.definition = {"_id": _id, "taskname": taskname, "description": description, "notes": notes,"status":status,
                           "percentagecomplete": percentagecomplete, "startdate": startdate, "duedate": duedate,
                           "completedate": completedate, "contactid": contactid, "ownerid": ownerid,
                           "milestoneid": milestoneid, "projectid": projectid, "contact": contact,
                           "ownername": ownername, "milestonename": milestonename, "projectname":projectname}

    def update_tasks(self, _id=None, taskname: str = None, description: str = None, notes: str = None,status:str = None,
                     percentagecomplete: str = None, startdate: str = None, duedate: str = None,completedate:str = None,
                     contactid: ObjectId = None, ownerid: ObjectId = None, milestoneid: ObjectId = None,
                     projectid: ObjectId = None, contact:Contacts = None, ownername:str = None, milestonename:str = None,
                     projectname:str = None):
        if _id is not None:
            if type(_id) is str:
                self.definition["_id"] = ObjectId(_id)
            elif type(_id) is ObjectId:
                self.definition["_id"] = _id
        if taskname is not None: self.definition["taskname"] = taskname
        if description is not None: self.definition["description"] = description
        if notes is not None: self.definition["notes"] = notes
        if status is not None: self.definition["status"] = status
        if percentagecomplete is not None: self.definition["percentagecomplete"] = percentagecomplete
        if startdate is not None: self.definition["startdate"] = startdate
        if duedate is not None: self.definition["duedate"] = duedate
        if completedate is not None: self.definition["completedate"] = completedate
        if contactid is not None: self.definition["contactid"] = contactid
        if ownerid is not None: self.definition["ownerid"] = ownerid
        if milestoneid is not None: self.definition["milestoneid"] = milestoneid
        if projectid is not None: self.definition["projectid"] = projectid
        if contact is not None: self.definition["contact"] = contact
        if ownername is not None: self.definition["ownername"] = ownername
        if milestonename is not None: self.definition["milestonename"] = milestonename
        if projectname is not None: self.definition["projectname"] = projectname

    # add by json string from query result
    def add_by_json(self, tasks_details):
        self.definition = tasks_details
