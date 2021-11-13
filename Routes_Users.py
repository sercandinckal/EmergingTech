
from flask import session, redirect, request, render_template
from DB_Projects import *
from DB_Tasks import *
from DB_Users import *

c_projects = ProjectsCollection("COLLAB")  # mongodb projects collection object
c_tasks = TasksCollection("COLLAB")  # mongodb task collection object
c_users = UsersCollection("COLLAB")  # mongodb user collection object


# home page/ login page
def route_login():
    # check if post or get request
    if request.method == "POST":
        username = request.values.get("username")
        password = request.values.get("password")
    else:
        username = request.args.get("username")
        password = request.args.get("password")
    if username is not None and password is not None:  # check its a login event if not skip checks and session
        user_details = c_users.validate_user(username, password)  # validate user
        if user_details is not None:
            user_details["date"] = now = datetime.now()  # in case we want expiring sessions
            session['user_details'] = user_details  # set session info for other pages
            return redirect("/dashboard")

    if "user_details" not in session:
        return render_template("main.html")
    else:
        return redirect("/dashboard")


# logout drops session info
def route_logout():
    session.pop('user_details', None)
    return redirect("/login")


# check if info in session is valid
def valid_user_access():
    if 'user_details' not in session:
        return {}  #no session details found
    return session['user_details']


# Routing for user endpoint
def route_users(id:str = None):
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        isprojmgr = True
        current_username = user_details.get("firstname")
        current_user_id = user_details.get('_id')
        projects = c_projects.get_all()
        users = c_users.get_all()
        tasks = c_tasks.get_all()
        return render_template("users.html", UserName=current_username, users=users, projects=projects,
                               tasks=tasks)
    elif user_details.get('accesstype') == 'Employee':
        return redirect("/dashboard")  # no access to users page
    else:
        session.pop('user_details', None)
        return redirect("/dashboard")  # no access to users page
