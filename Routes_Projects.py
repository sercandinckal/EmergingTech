
from flask import session, redirect, request, render_template
from DB_Projects import *
from DB_Tasks import *
from DB_Users import *

c_projects = ProjectsCollection("COLLAB")  # mongodb projects collection object
c_tasks = TasksCollection("COLLAB")  # mongodb task collection object
c_users = UsersCollection("COLLAB")  # mongodb user collection object


# check if info in session is valid
def valid_user_access():
    if 'user_details' not in session:
        return {}  #no session details found
    return session['user_details']


def route_projects(id:str = None, milestoneid:str = None):
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        isprojmgr = True
        current_username = user_details.get("firstname")
        current_user_id = user_details.get('_id')
        projects = c_projects.get_all()  # .get_by_prj_manager(current_user_id, status= "Active")
        milestones = c_projects.get_all_milestones()
        prjteam = c_projects.get_all_prjteam()
        tasks = c_tasks.get_all()
        return render_template("projects.html", UserName=current_username, isprojmgr=isprojmgr, projects=projects,
                               milestones=milestones, prjteam=prjteam, tasks=tasks)

    elif user_details.get('accesstype') == 'Employee':
        isprojmgr = False
        current_username = user_details.get("firstname")
        current_user_id = user_details.get('_id')
        projects = c_projects.get_all()  # .get_by_prj_manager(current_user_id, status= "Active")
        milestones = c_projects.get_all_milestones()
        prjteam = c_projects.get_all_prjteam()
        tasks = c_tasks.get_all()
        return render_template("projects.html", UserName=current_username, isprojmgr=isprojmgr, projects=projects,
                               milestones=milestones, prjteam=prjteam, tasks=tasks)
    else:
        session.pop('user_details', None)
        return redirect("/login")
