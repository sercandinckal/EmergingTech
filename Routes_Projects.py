import datetime

from dateutil.parser import parse

from bson import ObjectId
from flask import session, redirect, request, render_template, jsonify, abort
import DBCollections as DB
from DBDocuments import ProjectTeam, Milestones, Projects


# check if info in session is valid
def valid_user_access():
    if 'user_details' not in session:
        return {}  #no session details found
    return session['user_details']


# function behind main project page routing
def route_projects(id:str = None, milestoneid:str = None):
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        current_username = user_details.get("firstname")
        return render_template("projects.html", UserName=current_username, isprojmgr=True)

    elif user_details.get('accesstype') == 'Employee':
        current_username = user_details.get("firstname")
        current_user_id = user_details.get('_id')
        return render_template("projects.html", UserName=current_username, isprojmgr=False)
    else:
        session.pop('user_details', None)
        return redirect("/login")


# function behind get/post webservice  call
def createprjteam():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        # get request parameters
        if request.method == "POST":
            projectid = request.values.get("projectid")
            prjteamid = request.values.get("prjteamid")
            role = request.values.get("role")
        else:
            projectid = request.args.get("projectid")
            prjteamid = request.args.get("prjteamid")
            role = request.args.get("role")

        # test parameters
        try: role = role.strip()
        except: pass

        try:
            if prjteamid is not None and prjteamid.strip() != '':
                ObjectId(prjteamid)
            else: prjteamid = None
        except: prjteamid = None

        try:
            if projectid is not None and projectid.strip() != '':
                projectid = ObjectId(projectid.strip())
            else:  projectid = None
        except:  projectid = None

        # check if valid info was entered before trying to submit
        if prjteamid is not None:
            if DB.c_users.get_by_id(prjteamid) is not None:
                if projectid is not None:
                    if DB.c_projects.get_by_id(projectid) is not None:
                        prjteam = ProjectTeam(prjteamid=prjteamid, role=role)
                        response = DB.c_projects.insert_prjteam(projectid, prjteam)
                        if response is not None and response.modified_count>0:
                            return jsonify({"Success": "Inserted Record"})
                        else:
                            abort(400, 'Not Inserted')
                    else:
                        abort(400, 'Project doesnt exist')
                else:
                    abort(400, 'projectid was either left blank or ill formatted')
            else:
                abort(400, 'Team member doesnt exist')
        else:  abort(400, 'prjteamid was either left blank or ill formatted')
    else: abort(401)


# function behind get/post webservice  call
def getprjteam():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager' or user_details.get('accesstype') == 'Employee':
        if request.method == "POST":
            prjteamid = request.values.get("prjteamid")
            projectid = request.values.get("projectid")
        else:
            prjteamid = request.args.get("prjteamid")
            projectid = request.args.get("projectid")

        try:
            condition_str = {}
            if prjteamid is not None:
                condition_str['projectteam.prjteamid'] = ObjectId(prjteamid)
            if projectid is not None:
                condition_str['_id'] = ObjectId(projectid)
            prjteam = DB.c_projects.get_all_prjteam(condition_str=condition_str)
        except: prjteam=[]

        data = []
        for member in prjteam:
            member['_id'] = str(member['_id'])
            member['prjteamid'] = str(member['prjteamid'])
            member['projectid'] = str(member['projectid'])
            data.append(member)
        return jsonify(data)
    else:
        abort(401)


# function behind get/post webservice  call
def updateprjteam():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            projectid = request.values.get("projectid")
            prjteamidx = request.values.get("prjteamidx")
            prjteamid = request.values.get("prjteamid")
            role = request.values.get("role")
        else:
            projectid = request.args.get("projectid")
            prjteamidx = request.args.get("prjteamidx")
            prjteamid = request.args.get("prjteamid")
            role = request.args.get("role")

        try: role = role.strip()
        except: pass

        try:
            if prjteamid is not None and prjteamid.strip() != '':
                ObjectId(prjteamid)
            else: prjteamid = None
        except: prjteamid = None

        try:
            if projectid is not None and projectid.strip() != '':
                projectid = ObjectId(projectid.strip())
            else: projectid = None
        except: projectid = None

        try:
            if prjteamidx is not None:
                prjteamidx = int(prjteamidx)
        except: prjteamidx = None

        if prjteamid is not None:
            if projectid is not None:
                if prjteamidx is not None:
                    prjteam = ProjectTeam(prjteamid=prjteamid, role=role)
                    response = DB.c_projects.update_prjteam_by_idx(projectid, prjteamidx, prjteam)
                    if response is not None and response.modified_count > 0:
                        return jsonify({"Success": "Updated {0} records".format(response.modified_count)})
                    else:
                        abort(400, 'No update performed')
                else:
                    abort(400, 'prjteamidx was either left blank or not a number')
            else:
                abort(400, 'projectid was either left blank or ill formatted')
        else:
            abort(400, 'prjteamid was either left blank or ill formatted')
    else:
        abort(401)


# function behind get/post webservice  call
def deleteprjteam():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            projectid = request.values.get("projectid")
            prjteamid = request.values.get("prjteamid")
        else:
            projectid = request.args.get("projectid")
            prjteamid = request.args.get("prjteamid")
        try:
            if prjteamid is not None:
                ObjectId(prjteamid)
        except: prjteamid = None

        try:
            if projectid is not None:
                ObjectId(projectid)
        except: projectid = None

        if prjteamid is not None:
            if projectid is not None:
                # response = DB.c_projects.delete_prjteam(projectid,prjteamid)
                return jsonify({"Success": "Delete not working as yet"})
            else:
                abort(400, 'projectid was either left blank or ill-formatted')
        else:
            abort(400, 'prjteamid was either left blank or ill-formatted')
    else:
        abort(401)


# function behind get/post webservice  call
def createmilestones():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            projectid = request.values.get("projectid")
            milestonename = request.values.get("milestonename")
            duedate = request.values.get("duedate")
            status = request.values.get("status")
        else:
            projectid = request.args.get("projectid")
            milestonename = request.args.get("milestonename")
            duedate = request.args.get("duedate")
            status = request.args.get("status")

        milestoneid = ObjectId()
        try: milestonename = milestonename.strip()
        except: pass
        try: status = status.strip()
        except: pass
        try:
            if projectid is not None and projectid.strip() != '':
                projectid = ObjectId(projectid.strip())
            else: projectid = None
        except: projectid = None

        try:
            if duedate is not None:
                duedate = parse(duedate.strip())
        except: abort(400, 'duedate must be a valid date')

        if milestoneid is not None:
            if milestonename is not None:
                if projectid is not None:
                    if DB.c_projects.get_by_id(projectid) is not None:
                        milestone = Milestones(milestoneid=milestoneid, milestonename=milestonename, duedate=duedate,
                                               status=status)
                        response = DB.c_projects.insert_milestones(projectid, milestone)
                        if response is not None and response.modified_count>0:
                            return jsonify({"Success": str(milestoneid)})
                        else:
                            abort(400, 'Not Inserted')
                    else:
                        abort(400, 'Project does not exist')
                else:
                    abort(400, 'projectid was either left blank or ill formatted')
            else:
                abort(400, 'milestonename was either left blank or ill formatted')
        else:
            abort(400, 'milestoneid was either left blank or ill formatted')
    else:
        abort(401)


# function behind get/post webservice  call
def getmilestones():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager' or user_details.get('accesstype') == 'Employee':
        if request.method == "POST":
            milestoneid = request.values.get("milestoneid")
            projectid = request.values.get("projectid")
        else:
            milestoneid = request.args.get("milestoneid")
            projectid = request.args.get("projectid")
        try:
            condition_str = {}
            if milestoneid is not None:
                condition_str['milestones.milestoneid'] = ObjectId(milestoneid)
            if projectid is not None:
                condition_str['_id'] = ObjectId(projectid)
            milestones = DB.c_projects.get_all_milestones(condition_str=condition_str)
        except: milestones=[]

        data = []
        for milestone in milestones:
            milestone['_id'] = str(milestone['_id'])
            milestone['projectid'] = str(milestone['projectid'])
            milestone['milestoneid'] = str(milestone['milestoneid'])
            if milestone['duedate'] == datetime.datetime(1900,1,1):
                milestone['duedate'] = None
            else:
                milestone['duedate'] = str(milestone['duedate'])
            data.append(milestone)
        return jsonify(data)
    else:
        abort(401)


# function behind get/post webservice  call
def updatemilestones():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            projectid = request.values.get("projectid")
            milestoneidx = request.values.get("milestoneidx")
            milestoneid = request.values.get("milestoneid")
            milestonename = request.values.get("milestonename")
            duedate = request.values.get("duedate")
            status = request.values.get("status")
        else:
            projectid = request.args.get("projectid")
            milestoneidx = request.args.get("milestoneidx")
            milestoneid = request.args.get("milestoneid")
            milestonename = request.args.get("milestonename")
            duedate = request.args.get("duedate")
            status = request.args.get("status")

        try: milestonename = milestonename.strip()
        except: pass
        try: status = status.strip()
        except: pass

        try:
            if milestoneid is not None and milestoneid.strip() != '':
                ObjectId(milestoneid)
            else: milestoneid = None
        except: milestoneid = None

        try:
            if projectid is not None and projectid.strip() != '':
                projectid = ObjectId(projectid.strip())
            else: projectid = None
        except: projectid = None

        try:
            if milestoneidx is not None:
                milestoneidx = int(milestoneidx)
        except: milestoneidx = None

        try:
            if duedate is not None:
                duedate = parse(duedate.strip())
        except: abort(400, 'duedate must be a valid date')

        if milestoneid is not None:
            if projectid is not None:
                if milestoneidx is not None:
                    milestone = Milestones(milestoneid=milestoneid, milestonename=milestonename, duedate=duedate,
                                           status=status)
                    response = DB.c_projects.update_milestones_by_idx(projectid, milestoneidx, milestone)
                    if response is not None and response.modified_count > 0:
                        return jsonify({"Success": "Updated {0} records".format(response.modified_count)})
                    else:
                        abort(400, 'No update performed')
                else:
                    abort(400, 'milestoneidx was either left blank or not a number')
            else:
                abort(400, 'projectid was either left blank or ill formatted')
        else:
            abort(400, 'milestoneid was either left blank or ill formatted')
    else:
        abort(401)


# function behind get/post webservice  call
def deletemilestones():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            projectid = request.values.get("projectid")
            milestoneid = request.values.get("milestoneid")
        else:
            projectid = request.args.get("projectid")
            milestoneid = request.args.get("milestoneid")
        try:
            if milestoneid is not None:
                ObjectId(milestoneid)
        except: milestoneid = None

        try:
            if projectid is not None:
                ObjectId(projectid)
        except: projectid = None

        if milestoneid is not None:
            if projectid is not None:
                # response = DB.c_projects.delete_milestones(projectid,milestoneid)
                return jsonify({"Success": "Delete not working as yet"})
            else:
                abort(400, 'projectid was either left blank or ill-formatted')
        else:
            abort(400, 'milestoneid was either left blank or ill-formatted')
    else:
        abort(401)


# function behind get/post webservice  call
def createprojects():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            projectname = request.values.get("projectname")
            description = request.values.get("description")
            notes = request.values.get("notes")
            Status = request.values.get("Status")
            percentcomplete = request.values.get("percentcomplete")
            startdate = request.values.get("startdate")
            enddate = request.values.get("enddate")
            clientid = request.values.get("clientid")
            projectmanagerid = request.values.get("projectmanagerid")
        else:
            projectname = request.args.get("projectname")
            description = request.args.get("description")
            notes = request.args.get("notes")
            Status = request.args.get("Status")
            percentcomplete = request.args.get("percentcomplete")
            startdate = request.args.get("startdate")
            enddate = request.args.get("enddate")
            clientid = request.args.get("clientid")
            projectmanagerid = request.args.get("projectmanagerid")

        projectid = ObjectId()

        try: projectname = projectname.strip()
        except: pass
        try: description = description.strip()
        except: pass
        try: notes = notes.strip()
        except: pass
        try: Status = Status.strip()
        except: pass

        try:
            if clientid is not None and clientid.strip() != '':
                clientid = ObjectId(clientid.strip())
            else: clientid = None
        except: clientid = None

        try:
            if projectmanagerid is not None and projectmanagerid.strip() != '':
                projectmanagerid = ObjectId(projectmanagerid.strip())
            else: projectmanagerid = None
        except: projectmanagerid = None

        try:
            if startdate is not None:
                startdate = parse(startdate.strip())
        except: abort(400, 'startdate must be a valid date')

        try:
            if enddate is not None:
                enddate = parse(enddate.strip())
        except: abort(400, 'enddate must be a valid date')

        try:
            if percentcomplete is not None:
                percentcomplete = float(percentcomplete)
        except: abort(400, 'percentcomplete must be a valid number')

        if projectid is not None:
            if projectname is not None and projectname != "":
                if not list(DB.c_projects.get_by_projectname(projectname)):
                    if clientid is not None:
                        if DB.c_clients.get_by_id(clientid) is not None:
                            if projectmanagerid is not None:
                                if DB.c_users.get_by_id(projectmanagerid) is not None:
                                    project = Projects(_id=projectid, projectname=projectname, description=description,
                                                       notes=notes, Status=Status, percentcomplete=percentcomplete,
                                                       startdate=startdate,enddate=enddate, clientid=clientid,
                                                       projectmanagerid=projectmanagerid, projectteam=[], milestones=[])
                                    response = DB.c_projects.insert(project)
                                    if response is not None and response.inserted_id is not None:
                                        id = str(response.inserted_id)
                                        return jsonify({"Success": id})
                                    else:
                                        abort(400, 'Not Inserted')
                                else:
                                    abort(400, 'Project manager user doesnt exist')
                            else:
                                abort(400, 'projectmanagerid was either left blank or ill formatted')
                        else:
                            abort(400, 'Client doesnt exist')
                    else:
                        abort(400, 'clientid was either left blank or ill formatted')
                else:
                    abort(400, 'projectname already exist')
            else:
                abort(400, 'projectname was either left blank or ill formatted')
        else:
            abort(400, 'projectid was either left blank or ill formatted')
    else:
        abort(401)


# function behind get/post webservice  call
def getprojects():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager' or user_details.get('accesstype') == 'Employee':
        if request.method == "POST":
            projectid = request.values.get("projectid")
        else:
            projectid = request.args.get("projectid")

        try:
            condition_str = {}
            if projectid is not None:
                condition_str['_id'] = ObjectId(projectid)
            projects = DB.c_projects.get_all(condition_str=condition_str)
        except: projects=[]

        data = []
        for project in projects:
            project['_id'] = str(project['_id'])
            project['clientid'] = str(project['clientid'])
            if project['startdate'] == datetime.datetime(1900,1,1):
                project['startdate'] = None
            else:
                project['startdate'] = str(project['startdate'])
            if project['enddate'] == datetime.datetime(1900,1,1):
                project['enddate'] = None
            else:
                project['enddate'] = str(project['enddate'])
            project['projectmanagerid'] = str(project['projectmanagerid'])
            project['projectmanager']['_id'] = str(project['projectmanager']['_id'])
            project['client']['_id'] = str(project['client']['_id'])
            project['clientname'] = project['client']['clientname']
            project['projectteam'] = len(project['projectteam'])
            project['milestones'] = len(project['milestones'])
            project['percentcomplete'] = project['percentcomplete']
            data.append(project)
        return jsonify(data)
    else:
        abort(401)


# function behind get/post webservice  call
def updateprojects():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            projectid = request.values.get("projectid")
            projectname = request.values.get("projectname")
            description = request.values.get("description")
            notes = request.values.get("notes")
            Status = request.values.get("Status")
            percentcomplete = request.values.get("percentcomplete")
            startdate = request.values.get("startdate")
            enddate = request.values.get("enddate")
            clientid = request.values.get("clientid")
            projectmanagerid = request.values.get("projectmanagerid")
        else:
            projectid = request.args.get("projectid")
            projectname = request.args.get("projectname")
            description = request.args.get("description")
            notes = request.args.get("notes")
            Status = request.args.get("Status")
            percentcomplete = request.args.get("percentcomplete")
            startdate = request.args.get("startdate")
            enddate = request.args.get("enddate")
            clientid = request.args.get("clientid")
            projectmanagerid = request.args.get("projectmanagerid")

        try: projectname = projectname.strip()
        except: pass
        try: description = description.strip()
        except: pass
        try: notes = notes.strip()
        except: pass
        try: Status = Status.strip()
        except: pass

        try:
            if projectid is not None and projectid.strip() != '':
                ObjectId(projectid.strip())
            else: projectid = None
        except: projectid = None

        try:
            if clientid is not None and clientid.strip() != '':
                clientid = ObjectId(clientid.strip())
            else: clientid = None
        except: clientid = None

        try:
            if projectmanagerid is not None and projectmanagerid.strip() != '':
                projectmanagerid = ObjectId(projectmanagerid.strip())
            else: projectmanagerid = None
        except: projectmanagerid = None

        try:
            if startdate is not None:
                startdate = parse(startdate.strip())
        except: abort(400, 'startdate must be a valid date')
        try:
            if enddate is not None:
                enddate = parse(enddate.strip())
        except: abort(400, 'enddate must be a valid date')
        try:
            if percentcomplete is not None:
                percentcomplete = float(percentcomplete)
        except: abort(400, 'percentcomplete must be a valid number')

        if projectid is not None:
            if projectname is not None and projectname != "":
                if clientid is not None:
                    if projectmanagerid is not None:
                        prj = dict(DB.c_projects.get_by_id(projectid))
                        if len(prj) > 0:
                            project = Projects(_id=prj.get("_id"), projectname=prj.get("projectname"),
                                               description=prj.get("description"), notes=prj.get("notes"),
                                               Status=prj.get("Status"), percentcomplete=prj.get("percentcomplete"),
                                               startdate=prj.get("startdate"), enddate=prj.get("enddate"),
                                               clientid=prj.get("clientid"), projectmanagerid=prj.get("projectmanagerid"))

                            project.update_projects(_id=projectid, projectname=projectname, description=description,
                                                    notes=notes, Status=Status, percentcomplete=percentcomplete,
                                                    startdate=startdate, enddate=enddate, clientid=clientid,
                                                    projectmanagerid=projectmanagerid)
                            response = DB.c_projects.update_by_id(projectid, project)
                            if response is not None and response.modified_count > 0:
                                return jsonify({"Success": "Updated {0} records".format(response.modified_count)})
                            else:
                                abort(400, 'No update performed')
                        else:
                            abort(400, 'Project doesnt exist')
                    else:
                        abort(400, 'Projectmanagerid was either left blank or ill formatted')
                else:
                    abort(400, 'Clientid was either left blank or ill formatted')
            else:
                abort(400, 'projectname was either left blank or ill formatted')
        else:
            abort(400, 'Projectid was either left blank or ill formatted')
    else:
        abort(401)


# function behind get/post webservice  call
def deleteprojects():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            projectid = request.values.get("projectid")
        else:
            projectid = request.args.get("projectid")

        try:
            if projectid is not None:
                ObjectId(projectid)
        except: projectid = None

        if projectid is not None:
            # response = DB.c_projects.delete_by_id(projectid)
            return jsonify({"Success": "Delete not working as yet"})
        else:
            abort(400, 'projectid was either left blank or ill-formatted')
    else:
        abort(401)
