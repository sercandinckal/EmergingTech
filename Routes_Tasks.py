
from flask import session, redirect, request, render_template
from DB_Projects import *
from DB_Tasks import *

c_tasks = TasksCollection("COLLAB")  # mongodb task collection object
c_projects = ProjectsCollection("COLLAB")  # mongodb projects collection object

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
        projects = c_projects.get_all() #.get_by_prj_manager(current_user_id, status= "Active")
        tasks = c_tasks.get_all()
        try:
            projectdashboard = c_projects.get_my_dashboard(current_user_id).next()
        except: pass
        try:
            taskdashboard =c_tasks.get_pm_dashboard(current_user_id).next()
        except: pass
        return render_template("manager.html", UserName=current_username, projects=projects, tasks=tasks,
                               projectdashboard=projectdashboard, taskdashboard=taskdashboard, isprojmgr=isprojmgr)

    elif user_details.get('accesstype') == 'Employee':
        isprojmgr = False
        projectdashboard = {'count': 0, 'late': 0, 'upcoming': 0}
        taskdashboard = {'count': 0, 'late': 0, 'upcoming': 0}
        current_username = user_details.get('firstname')
        current_user_id = user_details.get('_id')
        projects = c_projects.get_all()  # .get_by_prj_manager(current_user_id, status= "Active")
        tasks = c_tasks.get_all()
        try:
            taskdashboard = c_tasks.get_pm_dashboard(current_user_id).next()
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
        isprojmgr = True
        current_username = user_details.get("firstname")
        current_user_id = user_details.get('_id')
        tasks = c_tasks.get_all()
        return render_template("tasks.html", UserName=current_username, isprojmgr=isprojmgr, tasks=tasks)
    elif user_details.get('accesstype') == 'Employee':
        isprojmgr = False
        current_username = user_details.get("firstname")
        current_user_id = user_details.get('_id')
        tasks = c_tasks.get_all()
        return render_template("tasks.html", UserName=current_username, isprojmgr=isprojmgr, tasks=tasks)
    else:
        session.pop('user_details', None)
        return redirect("/login")
