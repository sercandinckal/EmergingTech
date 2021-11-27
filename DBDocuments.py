from bson import ObjectId


class User:
    def __init__(self, _id=None, firstname: str = "", lastname: str = "", title: str = "", role: str = "",
                 email: str = "", phone: str = "", notes: str = "", usercode: str = "", accesstype: str = ""):
        if _id is not None:
            if type(_id) is str:
                _id = ObjectId(_id)
            else:
                _id = ObjectId()
        if firstname is None: firstname = ""
        if lastname is None: lastname = ""
        if title is None: title = ""
        if phone is None: phone = ""
        if email is None: email = ""
        if role is None: role = ""
        if usercode is None: usercode = ""
        if accesstype is None: accesstype = ""
        if notes is None: notes = ""
        self.definition = {"_id": _id, "firstname": firstname, "lastname": lastname, "title": title, "role": role,
                           "email": email, "phone": phone, "notes": notes, "usercode": usercode,
                           "accesstype": accesstype}

    def update_user(self, _id=None, firstname: str = None, lastname: str = None, title: str = None, role: str = None,
                    email: str = None, phone: str = None, notes: str = None, usercode: str = None,
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
        if accesstype is not None: self.definition["accesstype"] = accesstype


class Clients:
    def __init__(self, _id=None, clientname: str = "", industry: str = "", description: str = "",
                 phone: str = "", email: str = "", addr1: str = "", addr2: str = "", addr3: str = "",
                 country: str = "", notes: str = ""):
        if _id is not None:
            if type(_id) is str:
                _id = ObjectId(_id)
            else:
                _id = ObjectId()
        if clientname is None: clientname = ""
        if industry is None: industry = ""
        if description is None: description = ""
        if phone is None: phone = ""
        if email is None: email = ""
        if addr1 is None: addr1 = ""
        if addr2 is None: addr2 = ""
        if addr3 is None: addr3 = ""
        if country is None: country = ""
        if notes is None: notes = ""
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


class Contacts:
    def __init__(self, _id=None, firstname: str = "", lastname: str = "", title: str = "", role: str = "",
                 email: str = "", phone: str = "", notes: str = "", clientid: ObjectId = None):
        if _id is None:
            _id = ObjectId()
        else:
            if type(_id) is str:
                _id = ObjectId(_id)
        if firstname is None: firstname = ""
        if lastname is None: lastname = ""
        if title is None: title = ""
        if role is None: role = ""
        if email is None: email = ""
        if phone is None: phone = ""
        if notes is None: notes = ""

        self.definition = {"_id": _id, "firstname": firstname, "lastname": lastname, "title": title, "role": role,
                           "email": email, "phone": phone, "notes": notes, "clientid": clientid}

    def update_contact(self, _id=None, firstname: str = None, lastname: str = None, title: str = None, role: str = None,
                       email: str = None, phone: str = None, notes: str = None, clientid: ObjectId = None):
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


class ProjectTeam:
    def __init__(self, prjteamid=None, role: str = ""):
        if prjteamid is None:
            prjteamid = ObjectId()
        else:
            if type(prjteamid) is str:
                prjteamid = ObjectId(prjteamid)
        if role is None: role = ""
        self.definition = {"prjteamid": prjteamid, "role": role}

    def update_projectTeam(self, prjteamid=None, role: str = None, idx: int = None):
        if prjteamid is not None:
            if type(prjteamid) is str:
                self.definition["prjteamid"] = ObjectId(prjteamid)
            elif type(prjteamid) is ObjectId:
                self.definition["prjteamid"] = prjteamid
        if role is not None: self.definition["role"] = role
        if idx is not None: self.idx = idx


class Milestones:
    def __init__(self, milestoneid=None, milestonename: str = "", duedate: str = "", status: str = ""):
        if milestoneid is None:
            milestoneid = ObjectId()
        else:
            if type(milestoneid) is str:
                milestoneid = ObjectId(milestoneid)
        if milestonename is None: milestonename = ""
        if duedate is None: duedate = ""
        if status is None: status = ""
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


class Projects:
    def __init__(self, _id=None, projectname: str = "", description: str = "", notes: str = "", Status: str = "",
                 percentcomplete: str = "", startdate: str = "", enddate: str = "", clientid: ObjectId = None,
                 projectmanagerid: ObjectId = None, projectteam: [] = None, milestones: [] = None):
        if _id is None:
            _id = ObjectId()
        else:
            if type(_id) is str:
                _id = ObjectId(_id)
        if milestones is None: milestones = []
        if projectteam is None: projectteam = []
        if projectname is None: projectname = ""
        if description is None: description = ""
        if notes is None: notes = ""
        if Status is None: Status = ""
        if percentcomplete is None: percentcomplete = ""
        if startdate is None: startdate = ""
        if enddate is None: enddate = ""

        self.definition = {"_id": _id, "projectname": projectname, "description": description, "notes": notes,
                           "Status": Status, "percentcomplete": percentcomplete, "startdate": startdate,
                           "enddate": enddate, "clientid": clientid, "projectmanagerid": projectmanagerid}
        if projectteam is not None:
            self.definition["projectteam"] = projectteam
        if milestones is not None:
            self.definition["milestones"] = milestones

    def update_projects(self, _id=None, projectname: str = None, description: str = None, notes: str = None,
                        Status: str = None, percentcomplete: str = None, startdate: str = None, enddate: str = None,
                        clientid: object = None, projectmanagerid: ObjectId = None, projectteam: [] = None,
                        milestones: [] = None):
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
    def __init__(self, _id=None, taskname: str = "", description: str = "", notes: str = "", status: str = "",
                  percentagecomplete: str = "", startdate: str = "", duedate: str = "", completedate: str = "",
                  contactid: ObjectId = None, ownerid: ObjectId = None, milestoneid: ObjectId = None,
                  projectid: ObjectId = None):
        if _id is None:
            _id = ObjectId()
        else:
            if type(_id) is str:
                _id = ObjectId(_id)
        if taskname is None: taskname = ""
        if description is None: description = ""
        if notes is None: notes = ""
        if status is None: status = ""
        if percentagecomplete is None: percentagecomplete = ""
        if startdate is None: startdate = ""
        if duedate is None: duedate = ""
        if completedate is None: completedate = ""

        self.definition = {"_id": _id, "taskname": taskname, "description": description, "notes": notes,
                           "status": status, "percentagecomplete": percentagecomplete, "startdate": startdate,
                           "duedate": duedate, "completedate": completedate, "contactid": contactid, "ownerid": ownerid,
                           "milestoneid": milestoneid, "projectid": projectid}

    def update_tasks(self, _id=None, taskname: str = None, description: str = None, notes: str = None,
                     status: str = None,
                     percentagecomplete: str = None, startdate: str = None, duedate: str = None,
                     completedate: str = None,
                     contactid: ObjectId = None, ownerid: ObjectId = None, milestoneid: ObjectId = None,
                     projectid: ObjectId = None):
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
