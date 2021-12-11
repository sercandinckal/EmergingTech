from bson import ObjectId
from flask import session, redirect, request, render_template, jsonify, abort
import DBCollections as DB
from DBDocuments import ProjectTeam, Milestones, Projects


# check if info in session is valid
def valid_user_access():
    if 'user_details' not in session:
        return {}  #no session details found
    return session['user_details']


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


def createprjteam():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            projectid = request.values.get("projectid")
            prjteamid = request.values.get("prjteamid")
            role = request.values.get("role")
        else:
            projectid = request.args.get("projectid")
            prjteamid = request.args.get("prjteamid")
            role = request.args.get("role")

        try: projectid = ObjectId(projectid)
        except: projectid = None

        try: prjteamid = ObjectId(prjteamid)
        except: prjteamid = None

        if prjteamid is not None:
            if projectid is not None:
                prjteam = ProjectTeam(prjteamid=prjteamid, role=role)
                response = DB.c_projects.insert_prjteam(projectid, prjteam)
                if response.inserted_id is not None:
                    return jsonify({"Success": response.inserted_id})
                else:
                    abort(400, {'message': 'Not Inserted'})
            else:
                abort(400, {'message': 'projectid was either left blank or ill formatted'})
        else:
            abort(400, {'message': 'prjteamid was either left blank or ill formatted'})
    else:
        abort(401)


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
        except: pass

        data = []
        for member in prjteam:
            member['_id'] = str(member['_id'])
            member['prjteamid'] = str(member['prjteamid'])
            member['projectid'] = str(member['projectid'])
            data.append(member)
        return jsonify(data)
    else:
        abort(401)


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

        try: ObjectId(prjteamid)
        except: prjteamid = None

        try: projectid = ObjectId(projectid)
        except: projectid = None

        try: prjteamidx = int(prjteamidx)
        except: prjteamidx = None

        if prjteamid is not None:
            if projectid is not None:
                if prjteamidx is not None:
                    prjteam = ProjectTeam(prjteamid=prjteamid, role=role)
                    response = DB.c_projects.update_prjteam_by_idx(projectid, prjteamidx, prjteam)
                    if response.modified_count > 0:
                        return jsonify({"Success": "Updated " + response.modified_count + " records"})
                    else:
                        abort(400, {'message': 'No update performed'})
                else:
                    abort(400, {'message': 'prjteamidx was either left blank or not a number'})
            else:
                abort(400, {'message': 'projectid was either left blank or ill formatted'})
        else:
            abort(400, {'message': 'prjteamid was either left blank or ill formatted'})
    else:
        abort(401)


def deleteprjteam():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            projectid = request.values.get("projectid")
            prjteamid = request.values.get("prjteamid")
        else:
            projectid = request.args.get("projectid")
            prjteamid = request.args.get("prjteamid")
        try: ObjectId(prjteamid)
        except: prjteamid = None

        try: ObjectId(projectid)
        except: projectid = None

        if prjteamid is not None:
            if projectid is not None:
                # response = DB.c_projects.delete_prjteam(projectid,prjteamid)
                return jsonify({"Success": "Delete not working as yet"})
            else:
                abort(400, {'message': 'projectid was either left blank or ill-formatted'})
        else:
            abort(400, {'message': 'prjteamid was either left blank or ill-formatted'})
    else:
        abort(401)


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
        try: projectid = ObjectId(projectid)
        except: projectid = None

        if milestoneid is not None:
            if projectid is not None:
                milestone = Milestones(milestoneid=milestoneid, milestonename=milestonename, duedate=duedate,
                                       status=status)
                response = DB.c_projects.insert_milestones(projectid, milestone)
                if response.inserted_id is not None:
                    return jsonify({"Success": response.inserted_id})
                else:
                    abort(400, {'message': 'Not Inserted'})
            else:
                abort(400, {'message': 'projectid was either left blank or ill formatted'})
        else:
            abort(400, {'message': 'milestoneid was either left blank or ill formatted'})
    else:
        abort(401)


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
        except: pass

        data = []
        for milestone in milestones:
            milestone['_id'] = str(milestone['_id'])
            milestone['projectid'] = str(milestone['projectid'])
            milestone['milestoneid'] = str(milestone['milestoneid'])
            data.append(milestone)
        return jsonify(data)
    else:
        abort(401)


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

        try: ObjectId(milestoneid)
        except: milestoneid = None

        try: projectid = ObjectId(projectid)
        except: projectid = None

        try: milestoneidx = int(milestoneidx)
        except: milestoneidx = None

        if milestoneid is not None:
            if projectid is not None:
                if milestoneidx is not None:
                    milestone = Milestones(milestoneid=milestoneid, milestonename=milestonename, duedate=duedate,
                                           status=status)
                    response = DB.c_projects.update_milestones_by_idx(projectid, milestoneidx, milestone)
                    if response.modified_count > 0:
                        return jsonify({"Success": "Updated " + response.modified_count + " records"})
                    else:
                        abort(400, {'message': 'No update performed'})
                else:
                    abort(400, {'message': 'milestoneidx was either left blank or not a number'})
            else:
                abort(400, {'message': 'projectid was either left blank or ill formatted'})
        else:
            abort(400, {'message': 'milestoneid was either left blank or ill formatted'})
    else:
        abort(401)


def deletemilestones():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            projectid = request.values.get("projectid")
            milestoneid = request.values.get("milestoneid")
        else:
            projectid = request.args.get("projectid")
            milestoneid = request.args.get("milestoneid")
        try: ObjectId(milestoneid)
        except: milestoneid = None

        try: ObjectId(projectid)
        except: projectid = None

        if milestoneid is not None:
            if projectid is not None:
                # response = DB.c_projects.delete_milestones(projectid,milestoneid)
                return jsonify({"Success": "Delete not working as yet"})
            else:
                abort(400, {'message': 'projectid was either left blank or ill-formatted'})
        else:
            abort(400, {'message': 'milestoneid was either left blank or ill-formatted'})
    else:
        abort(401)


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

        try: clientid = ObjectId(clientid)
        except: clientid = None

        try: projectmanagerid = ObjectId(projectmanagerid)
        except: projectmanagerid = None

        if projectid is not None:
            if clientid is not None:
                if projectmanagerid is not None:
                    project = Projects(_id=projectid, projectname=projectname, description=description, notes=notes,
                                       Status=Status, percentcomplete=percentcomplete, startdate=startdate,
                                       enddate=enddate, clientid=clientid, projectmanagerid=projectmanagerid,
                                       projectteam=[], milestones=[])
                    response = DB.c_projects.insert(project)
                    if response.inserted_id is not None:
                        return jsonify({"Success": response.inserted_id})
                    else:
                        abort(400, {'message': 'Not Inserted'})
                else:
                    abort(400, {'message': 'Projectmanagerid was either left blank or ill formatted'})
            else:
                abort(400, {'message': 'Clientid was either left blank or ill formatted'})
        else:
            abort(400, {'message': 'Projectid was either left blank or ill formatted'})
    else:
        abort(401)


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
        except: pass

        data = []
        for project in projects:
            project['_id'] = str(project['_id'])
            project['clientid'] = str(project['clientid'])
            project['projectmanagerid'] = str(project['projectmanagerid'])
            project['projectmanager']['_id'] = str(project['projectmanager']['_id'])
            project['client']['_id'] = str(project['client']['_id'])
            project['clientname'] = project['client']['clientname']
            project['projectteam'] = len(project['projectteam'])
            project['milestones'] = len(project['milestones'])
            project['percentcomplete'] = float(project['percentcomplete'].to_decimal())
            data.append(project)
        return jsonify(data)
    else:
        abort(401)


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

        try: ObjectId(projectid)
        except: projectid = None

        try: clientid = ObjectId(clientid)
        except: clientid = None

        try: projectmanagerid = ObjectId(projectmanagerid)
        except: projectmanagerid = None

        if projectid is not None:
            if clientid is not None:
                if projectmanagerid is not None:
                    project = Projects(_id=projectid, projectname=projectname, description=description, notes=notes,
                                       Status=Status, percentcomplete=percentcomplete, startdate=startdate,
                                       enddate=enddate, clientid=clientid, projectmanagerid=projectmanagerid)
                    response = DB.c_projects.update_by_id(projectid, project)
                    if response.modified_count > 0:
                        return jsonify({"Success": "Updated " + response.modified_count + " records"})
                    else:
                        abort(400, {'message': 'No update performed'})
                else:
                    abort(400, {'message': 'Projectmanagerid was either left blank or ill formatted'})
            else:
                abort(400, {'message': 'Clientid was either left blank or ill formatted'})
        else:
            abort(400, {'message': 'Projectid was either left blank or ill formatted'})
    else:
        abort(401)


def deleteprojects():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            projectid = request.values.get("projectid")
        else:
            projectid = request.args.get("projectid")

        try: ObjectId(projectid)
        except: projectid = None

        if projectid is not None:
            # response = DB.c_projects.delete_by_id(projectid)
            return jsonify({"Success": "Delete not working as yet"})
        else:
            abort(400, {'message': 'projectid was either left blank or ill-formatted'})
    else:
        abort(401)
