"""
Hold main program structure of flask routes & webservice

-if you dont login all routes send you to login page
-All return <text> at routes to be replaced with templates html pages

"""

from flask import Flask, redirect, Response, jsonify
import secrets
import Routes_Clients
import Routes_Projects
import Routes_Tasks
import Routes_Users

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(128)

# #web pages
app.add_url_rule("/login", "login", Routes_Users.route_login, methods=['GET', 'POST'])
app.add_url_rule("/login/", "login", Routes_Users.route_login, methods=['GET', 'POST'])
app.add_url_rule("/logout", "logout", Routes_Users.route_logout)
app.add_url_rule("/logout/", "logout", Routes_Users.route_logout)

app.add_url_rule("/employees", "users", Routes_Users.route_users)
app.add_url_rule("/employees/", "users", Routes_Users.route_users)

app.add_url_rule("/projects", "projects", Routes_Projects.route_projects)
app.add_url_rule("/projects/", "projects", Routes_Projects.route_projects)

app.add_url_rule("/clients", "clients", Routes_Clients.route_clients)
app.add_url_rule("/clients/", "clients", Routes_Clients.route_clients)

app.add_url_rule("/dashboard", "dashboard", Routes_Tasks.route_dashboard)
app.add_url_rule("/dashboard/", "dashboard", Routes_Tasks.route_dashboard)

app.add_url_rule("/tasks", "tasks", Routes_Tasks.route_tasks)
app.add_url_rule("/tasks/", "tasks", Routes_Tasks.route_tasks)

# #web service
    # add / create
app.add_url_rule("/createclient", "createclient", Routes_Clients.createclients, methods=['GET', 'POST'])
app.add_url_rule("/createcontact", "createcontact", Routes_Clients.createcontacts, methods=['GET', 'POST'])
app.add_url_rule("/createproject", "createproject", Routes_Projects.createprojects, methods=['GET', 'POST'])
app.add_url_rule("/createmilestone", "createmilestone", Routes_Projects.createmilestones, methods=['GET', 'POST'])
app.add_url_rule("/createprjteam", "createprjteam", Routes_Projects.createprjteam, methods=['GET', 'POST'])
app.add_url_rule("/createtask", "createtask", Routes_Tasks.createtasks, methods=['GET', 'POST'])
app.add_url_rule("/createuser", "createuser", Routes_Users.createuser, methods=['GET', 'POST'])

    # get / read
app.add_url_rule("/getclients", "getclients", Routes_Clients.getclients, methods=['GET', 'POST'])
app.add_url_rule("/getcontacts", "getcontacts", Routes_Clients.getcontacts, methods=['GET', 'POST'])
app.add_url_rule("/getprojects", "getprojects", Routes_Projects.getprojects, methods=['GET', 'POST'])
app.add_url_rule("/getmilestones", "getmilestones", Routes_Projects.getmilestones, methods=['GET', 'POST'])
app.add_url_rule("/getprjteam", "getprjteam", Routes_Projects.getprjteam, methods=['GET', 'POST'])
app.add_url_rule("/gettasks", "gettasks", Routes_Tasks.gettasks, methods=['GET', 'POST'])
app.add_url_rule("/getusers", "getusers", Routes_Users.getusers, methods=['GET', 'POST'])

app.add_url_rule("/getclients/", "getclients", Routes_Clients.getclients, methods=['GET', 'POST'])
app.add_url_rule("/getcontacts/", "getcontacts", Routes_Clients.getcontacts, methods=['GET', 'POST'])
app.add_url_rule("/getprojects/", "getprojects", Routes_Projects.getprojects, methods=['GET', 'POST'])
app.add_url_rule("/getmilestones/", "getmilestones", Routes_Projects.getmilestones, methods=['GET', 'POST'])
app.add_url_rule("/getprjteam/", "getprjteam", Routes_Projects.getprjteam, methods=['GET', 'POST'])
app.add_url_rule("/gettasks/", "gettasks", Routes_Tasks.gettasks, methods=['GET', 'POST'])
app.add_url_rule("/getusers/", "getusers", Routes_Users.getusers, methods=['GET', 'POST'])


    # edit / update
app.add_url_rule("/updateclient", "updateclient", Routes_Clients.updateclients, methods=['GET', 'POST'])
app.add_url_rule("/updatecontact", "updatecontact", Routes_Clients.updatecontacts, methods=['GET', 'POST'])
app.add_url_rule("/updateproject", "updateproject", Routes_Projects.updateprojects, methods=['GET', 'POST'])
app.add_url_rule("/updatemilestone", "updatemilestone", Routes_Projects.updatemilestones, methods=['GET', 'POST'])
app.add_url_rule("/updateprjteam", "updateprjteam", Routes_Projects.updateprjteam, methods=['GET', 'POST'])
app.add_url_rule("/updatetask", "updatetask", Routes_Tasks.updatetasks, methods=['GET', 'POST'])
app.add_url_rule("/updateuser", "updateuser", Routes_Users.updateuser, methods=['GET', 'POST'])
app.add_url_rule("/updatepassword", "updatepassword", Routes_Users.updatepassword, methods=['GET', 'POST'])

    # delete
app.add_url_rule("/deleteclient", "deleteclient", Routes_Clients.deleteclients, methods=['GET', 'POST'])
app.add_url_rule("/deletecontact", "deletecontact", Routes_Clients.deletecontacts, methods=['GET', 'POST'])
app.add_url_rule("/deleteproject", "deleteproject", Routes_Projects.deleteprojects, methods=['GET', 'POST'])
app.add_url_rule("/deletemilestone", "deletemilestone", Routes_Projects.deletemilestones, methods=['GET', 'POST'])
app.add_url_rule("/deleteprjteam", "deleteprjteam", Routes_Projects.deleteprjteam, methods=['GET', 'POST'])
app.add_url_rule("/deletetask", "deletetask", Routes_Tasks.deletetasks, methods=['GET', 'POST'])
app.add_url_rule("/deleteuser", "deleteuser", Routes_Users.deleteuser, methods=['GET', 'POST'])


@app.errorhandler(400)
def route_custom400(error):
    return error.description


@app.errorhandler(401)
def route_unauthorized(error):
    return Response('Not Authorized to access')


@app.errorhandler(404)
def route_home(exception):
    return redirect("/login")


if __name__ == '__main__':
    app.run()
