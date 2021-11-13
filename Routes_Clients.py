
from flask import session, redirect, request, render_template
from DB_Clients import *
from DB_Projects import *
from DB_Tasks import *
from DB_Users import *

c_projects = ProjectsCollection("COLLAB")  # mongodb projects collection object
c_tasks = TasksCollection("COLLAB")  # mongodb projects collection object
c_users = UsersCollection("COLLAB")  # mongodb user collection object
c_clients = ClientsCollection("COLLAB")  # mongodb clients collection object
c_contacts = ContactsCollection("COLLAB")  # mongodb contacts collection object


# check if info in session is valid
def valid_user_access():
    if 'user_details' not in session:
        return {}  #no session details found
    return session['user_details']


def route_clients(id:str = None):
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        isprojmgr = True
        current_username = user_details.get("firstname")
        current_user_id = user_details.get('_id')
        projects = c_projects.get_all()
        clients = c_clients.get_all()
        contacts = c_contacts.get_all()
        return render_template("clients.html", UserName=current_username, clients=clients, contacts=contacts,
                               projects=projects)

    elif user_details.get('accesstype') == 'Employee':
        return redirect("/dashboard")  # no access to clients page
    else:
        session.pop('user_details', None)
        return redirect("/dashboard")# no access to clients page

