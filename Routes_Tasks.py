from bson import ObjectId
from flask import session, redirect, request, render_template, jsonify, abort
import DBCollections as DB
from DBDocuments import Tasks

# check if info in session is valid
def valid_user_access():
    if 'user_details' not in session:
        return {}  #no session details found
    return session['user_details']


# dashboard page
def route_dashboard():
    user_details = valid_user_access()

    if user_details.get('accesstype') == 'Proj Manager':
        isprojmgr = True
        projectdashboard = {'count': 0, 'late': 0, 'upcoming': 0}
        taskdashboard = {'count': 0, 'late': 0, 'upcoming': 0}
        current_username = user_details.get("firstname")
        current_user_id = user_details.get('_id')
        projects = DB.c_projects.get_all() #.get_by_prj_manager(current_user_id, status= "Active")
        tasks = DB.c_tasks.get_all()
        try:
            projectdashboard = DB.c_projects.get_my_dashboard(current_user_id).next()
        except: pass
        try:
            taskdashboard = DB.c_tasks.get_pm_dashboard(current_user_id).next()
        except: pass
        return render_template("manager.html", UserName=current_username, projects=projects, tasks=tasks,
                               projectdashboard=projectdashboard, taskdashboard=taskdashboard, isprojmgr=isprojmgr)

    elif user_details.get('accesstype') == 'Employee':
        isprojmgr = False
        projectdashboard = {'count': 0, 'late': 0, 'upcoming': 0}
        taskdashboard = {'count': 0, 'late': 0, 'upcoming': 0}
        current_username = user_details.get('firstname')
        current_user_id = user_details.get('_id')
        projects = DB.c_projects.get_all()  # .get_by_prj_manager(current_user_id, status= "Active")
        tasks = DB.c_tasks.get_all()
        try:
            taskdashboard = DB.c_tasks.get_pm_dashboard(current_user_id).next()
        except:
            pass
        return render_template("manager.html", UserName=current_username, projects=projects, tasks=tasks,
                               projectdashboard=projectdashboard, taskdashboard=taskdashboard, isprojmgr=isprojmgr)

    else:
        # session info is invalid, drop and ask to re login
        session.pop('user_details', None)
        return redirect("/login")


def route_tasks(id:str = None):
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        current_username = user_details.get("firstname")
        current_user_id = user_details.get('_id')
        return render_template("tasks.html", UserName=current_username, isprojmgr=True)
    elif user_details.get('accesstype') == 'Employee':
        current_username = user_details.get("firstname")
        current_user_id = user_details.get('_id')
        return render_template("tasks.html", UserName=current_username, isprojmgr=False)
    else:
        session.pop('user_details', None)
        return redirect("/login")


def createtasks():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            taskname = request.values.get("taskname")
            description = request.values.get("description")
            notes = request.values.get("notes")
            status = request.values.get("status")
            percentagecomplete = request.values.get("percentagecomplete")
            startdate = request.values.get("startdate")
            duedate = request.values.get("duedate")
            completedate = request.values.get("completedate")
            contactid = request.values.get("contactid")
            ownerid = request.values.get("ownerid")
            milestoneid = request.values.get("milestoneid")
            projectid = request.values.get("projectid")
        else:
            taskname = request.args.get("taskname")
            description = request.args.get("description")
            notes = request.args.get("notes")
            status = request.args.get("status")
            percentagecomplete = request.args.get("percentagecomplete")
            startdate = request.args.get("startdate")
            duedate = request.args.get("duedate")
            completedate = request.args.get("completedate")
            contactid = request.args.get("contactid")
            ownerid = request.args.get("ownerid")
            milestoneid = request.args.get("milestoneid")
            projectid = request.args.get("projectid")

        taskid = ObjectId()

        try: contactid = ObjectId(contactid)
        except: contactid = None

        try: ownerid = ObjectId(ownerid)
        except: ownerid = None

        try: milestoneid = ObjectId(milestoneid)
        except: milestoneid = None

        try: projectid = ObjectId(projectid)
        except: projectid = None

        if taskid is not None:
            if projectid is not None:
                if milestoneid is not None:
                    task = Tasks(_id=taskid, taskname=taskname, description=description, notes=notes, status=status,
                                 percentagecomplete=percentagecomplete, startdate=startdate, duedate=duedate,
                                 completedate=completedate, contactid=contactid, ownerid=ownerid, projectid=projectid,
                                 milestoneid=milestoneid)
                    response = DB.c_tasks.insert(task)
                    if response.inserted_id is not None:
                        return jsonify({"Success": response.inserted_id})
                    else:
                        abort(400, {'message': 'Not Inserted'})
                else:
                    abort(400, {'message': 'milestoneid was either left blank or ill formatted'})
            else:
                abort(400, {'message': 'projectid was either left blank or ill formatted'})
        else:
            abort(400, {'message': 'taskid was either left blank or ill formatted'})
    else:
        abort(401)


def gettasks():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager' or user_details.get('accesstype') == 'Employee':
        if request.method == "POST":
            projectid = request.values.get("projectid")
            taskid = request.values.get("taskid")
            milestoneid = request.values.get("milestoneid")
            ownerid = request.values.get("ownerid")
        else:
            projectid = request.args.get("projectid")
            taskid = request.args.get("taskid")
            milestoneid = request.args.get("milestoneid")
            ownerid = request.args.get("ownerid")
        try:
            condition_str = {}
            if taskid is not None:
                condition_str['_id'] = ObjectId(taskid)
            if milestoneid is not None:
                condition_str['milestoneid'] = ObjectId(milestoneid)
            if ownerid is not None:
                condition_str['ownerid'] = ObjectId(ownerid)
            if projectid is not None:
                condition_str['projectid'] = ObjectId(projectid)

            tasks = DB.c_tasks.get_all(condition_str=condition_str)
        except: pass

        data = []
        for task in tasks:
            task['_id'] = str(task.get('_id'))
            task['ownerid'] = str(task.get('ownerid'))
            task['milestoneid'] = str(task.get('milestoneid'))
            task['projectid'] = str(task.get('projectid'))
            if task['contactid'] == {}:
                task['contactid'] = None
                task['contact'] = {}
            else:
                task['contactid'] = str(task.get('contactid'))
                task['contact']['_id'] = str(task.get('contact').get('_id'))
                task['contact']['clientid'] = str(task.get('contact').get('clientid'))

            data.append(task)
        return jsonify(data)
    else:
        abort(401)


def updatetasks():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            taskid = request.values.get("taskid")
            taskname = request.values.get("taskname")
            description = request.values.get("description")
            notes = request.values.get("notes")
            status = request.values.get("status")
            percentagecomplete = request.values.get("percentagecomplete")
            startdate = request.values.get("startdate")
            duedate = request.values.get("duedate")
            completedate = request.values.get("completedate")
            contactid = request.values.get("contactid")
            ownerid = request.values.get("ownerid")
            milestoneid = request.values.get("milestoneid")
            projectid = request.values.get("projectid")
        else:
            taskid = request.args.get("taskid")
            taskname = request.args.get("taskname")
            description = request.args.get("description")
            notes = request.args.get("notes")
            status = request.args.get("status")
            percentagecomplete = request.args.get("percentagecomplete")
            startdate = request.args.get("startdate")
            duedate = request.args.get("duedate")
            completedate = request.args.get("completedate")
            contactid = request.args.get("contactid")
            ownerid = request.args.get("ownerid")
            milestoneid = request.args.get("milestoneid")
            projectid = request.args.get("projectid")

        try: ObjectId(taskid)
        except: taskid = None

        try: contactid = ObjectId(contactid)
        except: contactid = None

        try: ownerid = ObjectId(ownerid)
        except: ownerid = None

        try: milestoneid = ObjectId(milestoneid)
        except: milestoneid = None

        try: projectid = ObjectId(projectid)
        except: projectid = None

        if taskid is not None:
            if projectid is not None:
                if milestoneid is not None:
                    task = Tasks(_id=taskid, taskname=taskname, description=description, notes=notes, status=status,
                                 percentagecomplete=percentagecomplete, startdate=startdate, duedate=duedate,
                                 completedate=completedate, contactid=contactid, ownerid=ownerid, projectid=projectid,
                                 milestoneid=milestoneid)
                    response = DB.c_tasks.update_by_id(taskid, task)
                    if response.modified_count > 0:
                        return jsonify({"Success": "Updated " + response.modified_count + " records"})
                    else:
                        abort(400, {'message': 'No update performed'})
                else:
                    abort(400, {'message': 'milestoneid was either left blank or ill formatted'})
            else:
                abort(400, {'message': 'projectid was either left blank or ill formatted'})
        else:
            abort(400, {'message': 'taskid was either left blank or ill formatted'})
    else:
        abort(401)


def deletetasks():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            taskid = request.values.get("taskid")
        else:
            taskid = request.args.get("taskid")
        try:
            ObjectId(taskid)
        except:
            taskid = None
        if taskid is not None:
            # response = DB.c_tasks.delete_by_id(taskid)
            return jsonify({"Success": "Delete not working as yet"})
        else:
            abort(400, {'message': 'taskid was either left blank or ill-formatted'})
    else:
        abort(401)
