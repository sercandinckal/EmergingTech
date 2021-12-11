from bson import ObjectId
from dateutil.parser import parse
from flask import session, redirect, request, render_template, jsonify, abort
import DBCollections as DB
import datetime
from DBDocuments import Tasks


# check if info in session is valid
def valid_user_access():
    if 'user_details' not in session:
        return {}  # no session details found
    return session['user_details']


# function for dashboard page
def route_dashboard():
    user_details = valid_user_access()

    if user_details.get('accesstype') == 'Proj Manager':
        isprojmgr = True
        projectdashboard = {'count': 0, 'late': 0, 'upcoming': 0}
        taskdashboard = {'count': 0, 'late': 0, 'upcoming': 0}
        current_username = user_details.get("firstname")
        current_user_id = user_details.get('_id')
        projects = DB.c_projects.get_all()  # .get_by_prj_manager(current_user_id, status= "Active")
        tasks = DB.c_tasks.get_all()
        try:
            projectdashboard = DB.c_projects.get_my_dashboard(current_user_id).next()
        except:
            pass
        try:
            taskdashboard = DB.c_tasks.get_pm_dashboard(current_user_id).next()
        except:
            pass
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


# function for task page
def route_tasks(id: str = None):
    user_details = valid_user_access() # html session information
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


# function behind get/post webservice  call
def createtasks():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        # get parameter from user request
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

        # trim strings, check for valid date, & check entered objectid values are valid
        taskid = ObjectId()
        try:
            taskname = taskname.strip()
        except:
            pass
        try:
            description = description.strip()
        except:
            pass
        try:
            notes = notes.strip()
        except:
            pass
        try:
            status = status.strip()
        except:
            pass

        try:
            if contactid is not None and contactid.strip() != '':
                contactid = ObjectId(contactid.strip())
            else:
                contactid = None
        except:
            contactid = None

        try:
            if ownerid is not None and ownerid.strip() != '':
                ownerid = ObjectId(ownerid.strip())
            else:
                ownerid = None
        except:
            ownerid = None

        try:
            if milestoneid is not None and milestoneid.strip() != '':
                milestoneid = ObjectId(milestoneid.strip())
            else:
                milestoneid = None
        except:
            milestoneid = None

        try:
            if projectid is not None and projectid.strip() != '':
                projectid = ObjectId(projectid.strip())
            else:
                projectid = None
        except:
            projectid = None

        try:
            if startdate is not None:
                startdate = parse(startdate.strip())
        except:
            abort(400, 'startdate must be a valid date')

        try:
            if duedate is not None:
                duedate = parse(duedate.strip())
        except:
            abort(400, 'duedate must be a valid date')

        try:
            if completedate is not None:
                completedate = parse(duedate.strip())
        except:
            abort(400, 'completedate must be a valid date')

        try:
            if percentagecomplete is not None:
                percentagecomplete = float(percentagecomplete)
        except:
            abort(400, 'percentagecomplete must be a valid number')

        # check if information entered is valid and enough to create a task
        if taskid is not None:
            if taskname is not None and taskname != '':
                if projectid is not None:
                    if DB.c_projects.get_by_id(projectid) is not None:
                        if milestoneid is not None:
                            if list(DB.c_projects.get_by_milestoneid(milestoneid)):
                                if (ownerid is not None and DB.c_users.get_by_id(ownerid) is not None) or ownerid is \
                                        None:
                                    if (contactid is not None and DB.c_contacts.get_by_id(contactid) is not None) or \
                                            contactid is None:
                                        task = Tasks(_id=taskid, taskname=taskname, description=description,
                                                     notes=notes, status=status, percentagecomplete=percentagecomplete,
                                                     startdate=startdate, duedate=duedate, completedate=completedate,
                                                     contactid=contactid, ownerid=ownerid, projectid=projectid,
                                                     milestoneid=milestoneid)
                                        response = DB.c_tasks.insert(task)
                                        if response is not None and response.inserted_id is not None:
                                            id = str(response.inserted_id)
                                            return jsonify({"Success": id})
                                        else:
                                            abort(400, 'Not Inserted')
                                    else:
                                        abort(400, 'Contact doesnt exist')
                                else:
                                    abort(400, 'Owner doesnt exist')
                            else:
                                abort(400, 'Milestone doesnt exist')
                        else:
                            abort(400, 'milestoneid was either left blank or ill formatted')
                    else:
                        abort(400, 'Project doesnt exist')
                else:
                    abort(400, 'projectid was either left blank or ill formatted')
            else:
                abort(400, 'taskname was either left blank or ill formatted')
        else:
            abort(400, 'taskid was either left blank or ill formatted')
    else:
        abort(401)


# function behind get/post webservice  call
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
        except:
            tasks=[]

        data = []
        for task in tasks:
            task['_id'] = str(task.get('_id'))
            task['ownerid'] = str(task.get('ownerid'))
            task['milestoneid'] = str(task.get('milestoneid'))
            task['projectid'] = str(task.get('projectid'))
            if task['startdate'] == datetime.datetime(1900,1,1):
                task['startdate'] = None
            else:
                task['startdate'] = str(task['startdate'])

            if task['duedate'] == datetime.datetime(1900,1,1):
                task['duedate'] = None
            else:
                task['duedate'] = str(task['duedate'])

            if task['completedate'] == datetime.datetime(1900,1,1):
                task['completedate'] = None
            else:
                task['completedate'] = str(task['completedate'])

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


# function behind get/post webservice  call
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

        try:
            taskname = taskname.strip()
        except:
            pass
        try:
            description = description.strip()
        except:
            pass
        try:
            notes = notes.strip()
        except:
            pass
        try:
            status = status.strip()
        except:
            pass

        try:
            if taskid is not None and taskid.strip() != '':
                ObjectId(taskid.strip())
            else: taskid = None
        except:
            taskid = None

        try:
            if contactid is not None and contactid.strip() != '':
                contactid = ObjectId(contactid.strip())
            else:
                contactid = None
        except:
            contactid = None

        try:
            if ownerid is not None and ownerid.strip() != '':
                ownerid = ObjectId(ownerid.strip())
            else:
                ownerid = None
        except:
            ownerid = None

        try:
            if milestoneid is not None and milestoneid.strip() != '':
                milestoneid = ObjectId(milestoneid.strip())
            else:
                milestoneid = None
        except:
            milestoneid = None

        try:
            if projectid is not None and projectid.strip() != '':
                projectid = ObjectId(projectid.strip())
            else:
                projectid = None
        except:
            projectid = None

        try:
            if startdate is not None:
                startdate = parse(startdate.strip())
        except:
            abort(400, 'startdate must be a valid date')

        try:
            if duedate is not None:
                duedate = parse(duedate.strip())
        except:
            abort(400, 'duedate must be a valid date')

        try:
            if completedate is not None:
                completedate = parse(duedate.strip())
        except:
            abort(400, 'completedate must be a valid date')

        try:
            if percentagecomplete is not None:
                percentagecomplete = float(percentagecomplete)
        except:
            abort(400, 'percentagecomplete must be a valid number')

        if taskid is not None:
            if taskname is not None and taskname != '':
                if projectid is not None:
                    if DB.c_projects.get_by_id(projectid) is not None:
                        tsk = dict(DB.c_tasks.get_by_id(taskid))
                        if len(tsk) > 0:
                            task = Tasks(_id=tsk.get("_id"), taskname=tsk.get("taskname"), duedate=tsk.get("duedate"),
                                         startdate=tsk.get("startdate"),notes=tsk.get("notes"),status=tsk.get("status"),
                                         projectid=tsk.get("projectid"), description=tsk.get("description"),
                                         percentagecomplete=tsk.get("percentagecomplete"), ownerid=tsk.get("ownerid"),
                                         contactid=tsk.get("contactid"), completedate=tsk.get("completedate"),
                                         milestoneid=tsk.get("milestoneid"))
                            if (ownerid is not None and DB.c_users.get_by_id(ownerid) is not None) or ownerid is None:
                                if (contactid is not None and DB.c_contacts.get_by_id(contactid) is not None) or \
                                        contactid is None:
                                    task.update_tasks(_id=taskid, taskname=taskname, description=description,
                                                      notes=notes, status=status, percentagecomplete=percentagecomplete,
                                                      startdate=startdate, duedate=duedate, completedate=completedate,
                                                      contactid=contactid, ownerid=ownerid)  # , projectid=projectid, milestoneid=milestoneid)
                                    response = DB.c_tasks.update_by_id(taskid, task)
                                    if response is not None and response.modified_count > 0:
                                        return jsonify({"Success": "Updated {0} records".format(response.modified_count)})
                                    else:
                                        abort(400, 'No update performed')
                                else:
                                    abort(400, 'Contact doesnt exist')
                            else:
                                abort(400, 'Owner doesnt exist')
                        else:
                            abort(400, 'Task doesnt exist')
                    else:
                        abort(400, 'Project doesnt exist')
                else:
                    abort(400, 'projectid was either left blank or ill formatted')
            else:
                abort(400, 'taskname was either left blank or ill formatted')
        else:
            abort(400, 'taskid was either left blank or ill formatted')
    else:
        abort(401)


# function behind get/post webservice  call
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
            abort(400, 'taskid was either left blank or ill-formatted')
    else:
        abort(401)
