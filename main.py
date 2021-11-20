"""
Hold main program structure of flask routes

-if you dont login all routes send you to login page
-currently you can login by adding arguments to the login route, just ensure the credentials are in the mongoDB
    ie http://localhost/login?username=<username>&password=<password>
-logout using     http://localhost/logout
-All return <text> at routes to be replaced with templates html pages

"""

from flask import Flask, redirect
import secrets
# import Routes
import Routes_Clients
import Routes_Projects
import Routes_Tasks
import Routes_Users

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(128)

app.add_url_rule("/login", "login", Routes_Users.route_login, methods=['GET','POST'])
app.add_url_rule("/login/", "login", Routes_Users.route_login, methods=['GET','POST'])
app.add_url_rule("/logout", "logout", Routes_Users.route_logout)
app.add_url_rule("/logout/", "logout", Routes_Users.route_logout)

app.add_url_rule("/users", "users", Routes_Users.route_users)
app.add_url_rule("/users/", "users", Routes_Users.route_users)
app.add_url_rule("/users/<id>", "users", Routes_Users.route_users)


app.add_url_rule("/projects", "projects", Routes_Projects.route_projects)
app.add_url_rule("/projects/", "projects", Routes_Projects.route_projects)
app.add_url_rule("/projects/<id>", "projects", Routes_Projects.route_projects)
app.add_url_rule("/projects/<id>/<milestoneid>", "projects", Routes_Projects.route_projects)


app.add_url_rule("/clients", "clients", Routes_Clients.route_clients)
app.add_url_rule("/clients/", "clients", Routes_Clients.route_clients)
app.add_url_rule("/clients/<id>", "clients", Routes_Clients.route_clients)


app.add_url_rule("/dashboard", "dashboard", Routes_Tasks.route_dashboard)
app.add_url_rule("/dashboard/", "dashboard", Routes_Tasks.route_dashboard)

app.add_url_rule("/tasks", "tasks", Routes_Tasks.route_tasks)
app.add_url_rule("/tasks/", "tasks", Routes_Tasks.route_tasks)
app.add_url_rule("/tasks/<id>", "tasks", Routes_Tasks.route_tasks)


@app.errorhandler(404)
def route_home(exception):
    return redirect("/login")


if __name__ == '__main__':
    app.run()
