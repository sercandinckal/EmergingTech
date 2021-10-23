"""
Hold main program structure of flask routes

-if you dont login all routes send you to login page
-currently you can login by adding arguments to the login route, just ensure the credentials are in the mongoDB
    ie http://localhost/login?username=<username>&password=<password>
-logout using     http://localhost/logout
-All return <text> at routes to be replaced with templates html pages

"""

from flask import Flask, redirect # built in
import secrets  # builtin
import Routes   # we built

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(128)

app.add_url_rule("/dbtest", "dbtest", Routes.route_test)

app.add_url_rule("/login", "login", Routes.route_login)
app.add_url_rule("/logout", "logout", Routes.route_logout)
app.add_url_rule("/dashboard", "dashboard", Routes.route_dashboard)
app.add_url_rule("/projects", "projects", Routes.route_projects)
app.add_url_rule("/clients", "clients", Routes.route_clients)
app.add_url_rule("/users", "users", Routes.route_users)
app.add_url_rule("/tasks", "tasks", Routes.route_tasks)


@app.errorhandler(404)
def route_home(exception):
    return redirect("/login")


if __name__ == '__main__':
    app.run()
