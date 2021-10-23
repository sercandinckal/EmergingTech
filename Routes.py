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
from bson.json_util import dumps  # for data testing
from bson.objectid import ObjectId
import json


# home page/ login page
def route_login():
    # current accesstype: Proj Manager, Employee
    username = request.args.get("username")
    password = request.args.get("password")
    if username is not None and password is not None:  # check its a login event if not skip checks and session
        c_users = UsersCollection("COLLAB")  # created db collection object
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


# dashboard page
def route_dashboard():
    if 'user_details' not in session:
        return redirect("/login")  # redirect if no session details found
    # check if info in session is valid and redirect according
    user_details = session['user_details']
    if user_details.get('accesstype') == 'Proj Manager':
        current_username = user_details.get("firstname")
        return render_template("manager.html", UserName=current_username)
        # f"Project Manager Dashboard Page {user_details['firstname']} {user_details['lastname']}"  # dashboard page
    elif user_details.get('accesstype') == 'Employee':
        return f"Employee Dashboard Page {user_details['firstname']} {user_details['lastname']}"  # dashboard page
    else:
        # session info is invalid, drop and ask to re login
        session.pop('user_details', None)
        return redirect("/login")


def route_projects():
    if 'user_details' not in session:
        return redirect("/login")

    user_details = session['user_details']
    if user_details.get('accesstype') == 'Proj Manager':
        return "Project Manager Projects Page"  # projects page
    elif user_details.get('accesstype') == 'Employee':
        return "Employee Projects Page"  # projects page
    else:
        session.pop('user_details', None)
        return redirect("/login")


def route_tasks():
    if 'user_details' not in session:
        return redirect("/login")

    user_details = session['user_details']
    if user_details.get('accesstype') == 'Proj Manager':
        return "Project Manager Tasks Page"  # Tasks page
    elif user_details.get('accesstype') == 'Employee':
        return "Employee Tasks Page"  # tasks page
    else:
        session.pop('user_details', None)
        return redirect("/login")


def route_clients():
    if 'user_details' not in session:
        return redirect("/login")

    user_details = session['user_details']
    if user_details.get('accesstype') == 'Proj Manager':
        return "Client Page"  # clients page
    elif user_details.get('accesstype') == 'Employee':
        return redirect("/dashboard")  # no access to clients page
    else:
        session.pop('user_details', None)
        return redirect("/login")


def route_users():
    if 'user_details' not in session:
        return redirect("/login")

    user_details = session['user_details']
    if user_details.get('accesstype') == 'Proj Manager':
        return "User page"  # users page
    elif user_details.get('accesstype') == 'Employee':
        return redirect("/dashboard")  # no access to users page
    else:
        session.pop('user_details', None)
        return redirect("/login")
