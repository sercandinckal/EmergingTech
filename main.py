"""
Hold main program structure with flask routes(nb routes are case sensitive):

-if you dont login all routes send you to login page
-currently you can login by adding arguments to the login route, just ensure the credentials are in the mongoDB
    ie http://localhost/login?username=<username>&password=<password>
-logout using     http://localhost/logout
-All return <text> at routes to be replaced with templates html pages
"""

from flask import Flask, session, redirect, request, render_template
from datetime import datetime
from DBDocuments import *  # get our built classes
from bson.json_util import dumps # for data testing
import json

app = Flask(__name__)
app.secret_key = 'secret_key'

# connection string to mongoDB
conn_str = "mongodb+srv://sa:COLLAB_3444@cluster0.jseia.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


# home page/ login page
@app.route("/")
@app.route("/login")
def route_login():
    # current access_level: Proj Manager, Employee
    username = request.args.get("username")
    password = request.args.get("password")
    if username is not None and password is not None:  # check its a login event if not skip checks and session
        c_users = UsersCollection(conn_str, "COLLAB")  # created db collection object
        userdetails = c_users.validate_user(username, password)  # validate user
        if userdetails is not None:
            userdetails["date"] = now = datetime.now()  # in case we want expiring sessions
            session['userDetails'] =  userdetails  # set session info for other pages
            return redirect("/dashboard")

    if "userDetails" not in session:
        return render_template("main.html")
        #return "Login Page"
    else:
        return redirect("/dashboard")


# logout drops session info
@app.route("/logout")
def route_logout():
    session.pop('userDetails', None)
    return redirect("/login")


# dashboard page
@app.route("/dashboard")
def route_dashboard():
    if 'userDetails' not in session:
        return redirect("/login") # redirect if no session details found
    # check if info in session is valid and redirect according
    userdetails = session['userDetails']
    if userdetails.get('access_level') == 'Proj Manager':
        return render_template("manager.html")
        # f"Project Manager Dashboard Page {userdetails['firstname']} {userdetails['lastname']}"  # dashboard page
    elif userdetails.get('access_level') == 'Employee':
        return f"Employee Dashboard Page {userdetails['firstname']} {userdetails['lastname']}"  # dashboard page
    else:
        # session info is invalid, drop and ask to re login
        session.pop('userDetails', None)
        return redirect("/login")


@app.route("/projects")
def route_projects():
    if 'userDetails' not in session:
        return redirect("/login")

    userdetails = session['userDetails']
    if userdetails.get('access_level') == 'Proj Manager':
        return "Project Manager Projects Page"  # projects page
    elif userdetails.get('access_level') == 'Employee':
        return "Employee Projects Page"  # projects page
    else:
        session.pop('userDetails', None)
        return redirect("/login")


@app.route("/tasks")
def route_tasks():
    if 'userDetails' not in session:
        return redirect("/login")

    userdetails = session['userDetails']
    if userdetails.get('access_level') == 'Proj Manager':
        return "Project Manager Tasks Page"  # Tasks page
    elif userdetails.get('access_level') == 'Employee':
        return "Employee Tasks Page"  # tasks page
    else:
        session.pop('userDetails', None)
        return redirect("/login")


@app.route("/clients")
def route_clients():
    if 'userDetails' not in session:
        return redirect("/login")

    userdetails = session['userDetails']
    if userdetails.get('access_level') == 'Proj Manager':
        return "Client Page"  # clients page
    elif userdetails.get('access_level') == 'Employee':
        return redirect("/dashboard") # no access to clients page
    else:
        session.pop('userDetails', None)
        return redirect("/login")


@app.route("/users")
def route_users():
    if 'userDetails' not in session:
        return redirect("/login")

    userdetails = session['userDetails']
    if userdetails.get('access_level') == 'Proj Manager':
        return "User page"  # users page
    elif userdetails.get('access_level') == 'Employee':
        return redirect("/dashboard") # no access to users page
    else:
        session.pop('userDetails', None)
        return redirect("/login")


if __name__ == '__main__':
    app.run()
