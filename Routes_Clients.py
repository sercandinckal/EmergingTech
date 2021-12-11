'''
Class in functions behind function of Client & Contacts routes
'''
from bson import ObjectId
from flask import session, redirect, request, render_template, jsonify, abort
import DBCollections as DB
from DBDocuments import Clients, Contacts


# check if info in session is valid
def valid_user_access():
    if 'user_details' not in session:
        return {}  # no session details found
    return session['user_details']


# main route to display the client web page
def route_clients(id: str = None):
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        isprojmgr = True
        current_username = user_details.get("firstname")
        current_user_id = user_details.get('_id')
        return render_template("clients.html", UserName=current_username)

    elif user_details.get('accesstype') == 'Employee':
        return redirect("/dashboard")  # no access to clients page
    else:
        session.pop('user_details', None)
        return redirect("/dashboard")  # no access to clients page


# function behind the create client webservice call
# works for both get & post
def createclients():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        # get paramters from call
        if request.method == "POST":
            clientname = request.values.get("clientname")
            industry = request.values.get("industry")
            description = request.values.get("description")
            phone = request.values.get("phone")
            email = request.values.get("email")
            addr1 = request.values.get("addr1")
            addr2 = request.values.get("addr2")
            addr3 = request.values.get("addr3")
            country = request.values.get("country")
            notes = request.values.get("notes")
        else:
            clientname = request.args.get("clientname")
            industry = request.args.get("industry")
            description = request.args.get("description")
            phone = request.args.get("phone")
            email = request.args.get("email")
            addr1 = request.args.get("addr1")
            addr2 = request.args.get("addr2")
            addr3 = request.args.get("addr3")
            country = request.args.get("country")
            notes = request.args.get("notes")

        #trim entries & check if objectids are valid
        try: clientname = clientname.strip()
        except: pass
        try: industry = industry.strip()
        except: pass
        try: description = description.strip()
        except: pass
        try: phone = phone.strip()
        except: pass
        try: email = email.strip()
        except: pass
        try: addr1 = addr1.strip()
        except: pass
        try: addr2 = addr2.strip()
        except: pass
        try: addr3 = addr3.strip()
        except: pass
        try: country = country.strip()
        except: pass
        try: notes = notes.strip()
        except: pass

        # create new object id for client
        clientid = ObjectId()

        # check if entered paramters meet requirements for submit
        if clientid is not None:
            if clientname is not None and clientname.strip() != '':
                if DB.c_clients.get_by_clientname(clientname) is None:
                    client = Clients(_id=clientid, clientname=clientname, industry=industry, description=description,
                                     phone=phone, email=email, addr1=addr1, addr2=addr2, addr3=addr3, country=country,
                                     notes=notes)
                    response = DB.c_clients.insert(client)
                    if response is not None and response.inserted_id is not None:
                        id = str(response.inserted_id)
                        return jsonify({"Success": id})
                    else:
                        abort(400, 'Not Inserted')
                else:
                    abort(400, 'Client already exist')
            else:
                abort(400, 'clientname was either left blank or ill formatted')
        else:
            abort(400, 'Clientid was either left blank or ill formatted')
    else:
        abort(401)


# function behind get/post webservice  call
def getclients():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            clientid = request.values.get("clientid")
        else:
            clientid = request.args.get("clientid")

        try:
            condition_str = {}
            if clientid is not None:
                condition_str['_id'] = ObjectId(clientid)

            clients = DB.c_clients.get_all(condition_str=condition_str)
        except:
            clients=[]

        data = []
        for client in clients:
            client['_id'] = str(client['_id'])
            data.append(client)
        return jsonify(data)
    else:
        abort(401)


# function behind get/post webservice  call
def updateclients():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            clientid = request.values.get("clientid")
            clientname = request.values.get("clientname")
            industry = request.values.get("industry")
            description = request.values.get("description")
            phone = request.values.get("phone")
            email = request.values.get("email")
            addr1 = request.values.get("addr1")
            addr2 = request.values.get("addr2")
            addr3 = request.values.get("addr3")
            country = request.values.get("country")
            notes = request.values.get("notes")
        else:
            clientid = request.args.get("clientid")
            clientname = request.args.get("clientname")
            industry = request.args.get("industry")
            description = request.args.get("description")
            phone = request.args.get("phone")
            email = request.args.get("email")
            addr1 = request.args.get("addr1")
            addr2 = request.args.get("addr2")
            addr3 = request.args.get("addr3")
            country = request.args.get("country")
            notes = request.args.get("notes")

        try:
            if clientid is not None and clientid.strip() != '':
                ObjectId(clientid)
            else:
                clientid = None
        except: clientid= None
        try: clientname = clientname.strip()
        except: pass
        try: industry = industry.strip()
        except: pass
        try: description = description.strip()
        except: pass
        try: phone = phone.strip()
        except: pass
        try: email = email.strip()
        except: pass
        try: addr1 = addr1.strip()
        except: pass
        try: addr2 = addr2.strip()
        except: pass
        try: addr3 = addr3.strip()
        except: pass
        try: country = country.strip()
        except: pass
        try: notes = notes.strip()
        except: pass

        if clientid is not None:
            if clientname is not None and clientname.strip() != '':
                cln = dict(DB.c_clients.get_by_id(clientid))
                if len(cln) > 0:
                    client = Clients(_id=cln.get("_id"), clientname=cln.get("clientname"), industry=cln.get("industry"),
                                     description=cln.get("description"), phone=cln.get("phone"), email=cln.get("email"),
                                     addr1=cln.get("addr1"), addr2=cln.get("addr2"), addr3=cln.get("addr3"),
                                     country=cln.get("country"), notes=cln.get("notes"))

                    client.update_client(_id=clientid, clientname=clientname, industry=industry, country=country,
                                         description=description, phone=phone, email=email, addr1=addr1, addr2=addr2,
                                         addr3=addr3, notes=notes)
                    response = DB.c_clients.update_by_id(clientid, client)
                    if response is not None and response.modified_count > 0:
                        return jsonify({"Success": "Updated {0} records".format(response.modified_count)})
                    else:
                        abort(400, 'No update performed')
                else:
                    abort(400, 'Client doesnt exist')
            else:
                abort(400, 'clientname was either left blank or ill formatted')
        else:
            abort(400, 'Clientid was either left blank or ill formatted')
    else:
        abort(401)


# function behind get/post webservice  call
def deleteclients():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            clientid = request.values.get("clientid")
        else:
            clientid = request.args.get("clientid")
        try:
            ObjectId(clientid)
        except:
            clientid = None
        if clientid is not None:
            #response = DB.c_clients.delete_by_id(clientid)
            return jsonify({"Success": "Delete not working as yet"})
        else:
            abort(400, 'Clientid was either left blank or ill-formatted')
    else:
        abort(401)


# function behind get/post webservice  call
def createcontacts():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            firstname = request.values.get("firstname")
            lastname = request.values.get("lastname")
            title = request.values.get("title")
            role = request.values.get("role")
            email = request.values.get("email")
            phone = request.values.get("phone")
            notes = request.values.get("notes")
            clientid = request.values.get("clientid")
        else:
            firstname = request.args.get("firstname")
            lastname = request.args.get("lastname")
            title = request.args.get("title")
            role = request.args.get("role")
            email = request.args.get("email")
            phone = request.args.get("phone")
            notes = request.args.get("notes")
            clientid = request.args.get("clientid")

        contactid = ObjectId()
        try:
            if clientid is not None and clientid.strip() != '':
                clientid = ObjectId(clientid.strip())
            else: clientid = None
        except:
            clientid = None

        try:
            firstname = firstname.strip()
        except:
            pass
        try:
            lastname = lastname.strip()
        except:
            pass
        try:
            title = title.strip()
        except:
            pass
        try:
            role = role.strip()
        except:
            pass
        try:
            email = email.strip()
        except:
            pass
        try:
            phone = phone.strip()
        except:
            pass
        try:
            notes = notes.strip()
        except:
            pass

        if clientid is not None:
            if DB.c_clients.get_by_id(clientid) is not None:
                if firstname is not None and firstname.strip() != '':
                    if lastname is not None and lastname.strip() != '':
                        contact = Contacts(_id=contactid, firstname=firstname, lastname=lastname, title=title, phone=phone,
                                           email=email, role=role, notes=notes, clientid=clientid)
                        response = DB.c_contacts.insert(contact)
                        if response is not None and response.inserted_id is not None:
                            id = str(response.inserted_id)
                            return jsonify({"Success": id})
                        else:
                            abort(400, 'Not Inserted')
                    else:
                        abort(400, 'lastname was either left blank or ill formatted')
                else:
                    abort(400, 'firstname was either left blank or ill formatted')
            else:
                abort(400, 'Client not valid')
        else:
            abort(400, 'clientid was either left blank or ill formatted')
    else:
        abort(401)


# function behind get/post webservice  call
def getcontacts():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager' or user_details.get('Employee') == 'Employee':
        if request.method == "POST":
            clientid = request.values.get("clientid")
            contactid = request.values.get("contactid")
            projectid = request.values.get("projectid")
        else:
            clientid = request.args.get("clientid")
            contactid = request.args.get("contactid")
            projectid = request.args.get("projectid")

        try:
            condition_str = {}
            if contactid is not None:
                condition_str['_id'] = ObjectId(contactid)
            if clientid is not None:
                condition_str['clientid'] = ObjectId(clientid)
            if projectid is not None:
                condition_str['projects._id'] = ObjectId(projectid)

            contacts = DB.c_contacts.get_all(condition_str=condition_str)
        except:
            contacts =[]

        data = []
        for contact in contacts:
            contact['_id'] = str(contact['_id'])
            contact['clientid'] = str(contact['clientid'])
            contact['client']['_id'] = str(contact['client']['_id'])

            data.append(contact)
        return jsonify(data)
    else:
        abort(401)


# function behind get/post webservice  call
def deletecontacts():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            contactid = request.values.get("contactid")
        else:
            contactid = request.args.get("contactid")
        try:
            ObjectId(contactid)
        except:
            contactid = None
        if contactid is not None:
            #response = DB.c_contacts.delete_by_id(contactid)
            return jsonify({"Success": "Delete not working as yet"})
        else:
            abort(400, 'Contactid was either left blank or ill-formatted')
    else:
        abort(401)


# function behind get/post webservice  call
def updatecontacts():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':

        if request.method == "POST":
            contactid = request.values.get("contactid")
            firstname = request.values.get("firstname")
            lastname = request.values.get("lastname")
            title = request.values.get("title")
            role = request.values.get("role")
            email = request.values.get("email")
            phone = request.values.get("phone")
            notes = request.values.get("notes")
            clientid = request.values.get("clientid")
        else:
            contactid = request.args.get("contactid")
            firstname = request.args.get("firstname")
            lastname = request.args.get("lastname")
            title = request.args.get("title")
            role = request.args.get("role")
            email = request.args.get("email")
            phone = request.args.get("phone")
            notes = request.args.get("notes")
            clientid = request.args.get("clientid")

        try:
            if contactid is not None and contactid.strip() != '':
                ObjectId(contactid.strip())
            else: contactid = None
        except: contactid = None

        try:
            if clientid is not None and clientid.strip() != '':
                clientid = ObjectId(clientid.strip())
            else: clientid = None
        except: clientid = None

        try: firstname = firstname.strip()
        except: pass
        try: lastname = lastname.strip()
        except: pass
        try: title = title.strip()
        except: pass
        try: role = role.strip()
        except: pass
        try: email = email.strip()
        except: pass
        try: phone = phone.strip()
        except: pass
        try: notes = notes.strip()
        except: pass

        if contactid is not None:
            if clientid is not None:
                if DB.c_clients.get_by_id(clientid) is not None:
                    if firstname is not None and firstname.strip() != '':
                        if lastname is not None and lastname.strip() != '':
                            cnt = dict(DB.c_contacts.get_by_id(contactid))
                            if len(cnt) > 0:
                                contact = Contacts(_id=cnt.get("_id"), firstname=cnt.get("firstname"),
                                                   lastname=cnt.get("lastname"), title=cnt.get("title"),
                                                   phone=cnt.get("phone"), email=cnt.get("email"), role=cnt.get("role"),
                                                   notes=cnt.get("notes"), clientid=cnt.get("clientid"))
                                contact.update_contact(_id=contactid, firstname=firstname, lastname=lastname,
                                                       title=title, phone=phone, email=email, role=role, notes=notes,
                                                       clientid=clientid)
                                response = DB.c_contacts.update_by_id(contactid, contact)
                                if response is not None and response.modified_count > 0:
                                    return jsonify({"Success": "Updated {0} records".format(response.modified_count)})
                                else:
                                    abort(400, 'No update performed')
                            else:
                                abort(400, 'Contact doesnt exist')
                        else:
                            abort(400, 'lastname was either left blank or ill formatted')
                    else:
                        abort(400, 'firstname was either left blank or ill formatted')
                else:
                    abort(400, 'Client not valid')
            else:
                abort(400, 'Clientid was either left blank or ill formatted')
        else:
            abort(400, 'Contactid was either left blank or ill formatted')
    else:
        abort(401)
