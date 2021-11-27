from DB_Clients import *
from DB_Projects import *
from DB_Tasks import *
from DB_Users import *

c_projects = ProjectsCollection("COLLAB")  # mongodb projects collection object
c_tasks = TasksCollection("COLLAB")  # mongodb projects collection object
c_users = UsersCollection("COLLAB")  # mongodb user collection object
c_clients = ClientsCollection("COLLAB")  # mongodb clients collection object
c_contacts = ContactsCollection("COLLAB")  # mongodb contacts collection object