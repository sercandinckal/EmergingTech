from bson import ObjectId
from datetime import datetime
from flask import session, redirect, request, render_template, jsonify, abort
import DBCollections as DB
from DBDocuments import User


# home page/ login page
def route_login():
    # check if post or get request
    val = request.values
    args = request.args
    if request.method == "POST":
        email = request.values.get("email")
        password = request.values.get("password")
    else:
        email = request.args.get("email")
        password = request.args.get("password")

    if email is not None and password is not None:  # check its a login event if not skip checks and session
        user_details = DB.c_users.validate_by_email(email, password)  # validate user
        if user_details is not None:
            user_details["date"] = datetime.now()  # in case we want expiring sessions
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
        current_username = user_details.get("firstname")
        current_user_id = user_details.get('_id')
        return render_template("users.html", UserName=current_username)
    elif user_details.get('accesstype') == 'Employee':
        return redirect("/dashboard")  # no access to users page
    else:
        session.pop('user_details', None)
        return redirect("/dashboard")  # no access to users page


def createuser():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            firstname = request.values.get("firstname")
            lastname = request.values.get("lastname ")
            title = request.values.get("title")
            role = request.values.get("role")
            email = request.values.get("email ")
            phone = request.values.get("phone ")
            notes = request.values.get("notes ")
            usercode = request.values.get("usercode")
            accesstype = request.values.get("accesstype")
            password = request.values.get("password")
        else:
            firstname = request.args.get("firstname")
            lastname = request.args.get("lastname ")
            title = request.args.get("title")
            role = request.args.get("role")
            email = request.args.get("email ")
            phone = request.args.get("phone ")
            notes = request.args.get("notes ")
            usercode = request.args.get("usercode")
            accesstype = request.args.get("accesstype")
            password = request.args.get("password")

        userid = ObjectId()

        if userid is not None:
            user = User(_id=userid, firstname=firstname, lastname=lastname, title=title, role=role, phone=phone,
                        email=email, usercode=usercode, accesstype=accesstype, notes=notes)
            response = DB.c_users.insert(user)
            if response.inserted_id is not None:
                DB.c_users.reset_password_by_id(userid, password)
                return jsonify({"Success": response.inserted_id})
            else:
                abort(400, {'message': 'Not Inserted'})
        else:
            abort(400, {'message': 'Userid was either left blank or ill formatted'})
    else:
        abort(401)


def getusers():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            userid = request.values.get("userid")
        else:
            userid = request.args.get("userid")
        condition_str = {}
        try:
            if userid is not None:
                condition_str['_id'] = ObjectId(userid)
            users = DB.c_users.get_all(condition_str=condition_str)
        except: pass

        data = []
        for user in users:
            user['_id'] = str(user['_id'])
            data.append(user)
        return jsonify(data)
    else:
        abort(401)


def updatepassword():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            userid = request.values.get("userid")
            password = request.values.get("password")
        else:
            userid = request.args.get("userid")
            password = request.args.get("password")

        try: ObjectId(userid)
        except: userid = None
        if password is not None and password.strip() == 0:
            password=None

        if password is not None:
            if userid is not None:
                response = DB.c_users.reset_password_by_id(userid, password)
                if response.modified_count > 0:
                    return jsonify({"Success": "Updated password"})
                else:
                    abort(400, {'message': 'Password not reset'})
            else:
                abort(400, {'message': 'Userid was either left blank or ill formatted'})
        else:
            abort(400, {'message': 'Password was either left blank or ill formatted'})
    else:
        abort(401)


def updateuser():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            userid = request.values.get("userid")
            firstname = request.values.get("firstname")
            lastname = request.values.get("lastname ")
            title = request.values.get("title")
            role = request.values.get("role")
            email = request.values.get("email ")
            phone = request.values.get("phone ")
            notes = request.values.get("notes ")
            usercode = request.values.get("usercode")
            accesstype = request.values.get("accesstype")
        else:
            userid = request.args.get("userid")
            firstname = request.args.get("firstname")
            lastname = request.args.get("lastname ")
            title = request.args.get("title")
            role = request.args.get("role")
            email = request.args.get("email ")
            phone = request.args.get("phone ")
            notes = request.args.get("notes ")
            usercode = request.args.get("usercode")
            accesstype = request.args.get("accesstype")

        try:
            ObjectId(userid)
        except:
            userid = None
        if userid is not None:
            user = User(_id=userid, firstname=firstname, lastname=lastname, title=title, role=role, phone=phone,
                        email=email, usercode=usercode, accesstype=accesstype, notes=notes)
            response = DB.c_users.update_by_id(userid, user)
            if response.modified_count > 0:
                return jsonify({"Success": "Updated " + response.modified_count + " records"})
            else:
                abort(400, {'message': 'No update performed'})
        else:
            abort(400, {'message': 'Userid was either left blank or ill formatted'})
    else:
        abort(401)


def deleteuser():
    user_details = valid_user_access()
    if user_details.get('accesstype') == 'Proj Manager':
        if request.method == "POST":
            userid = request.values.get("userid")
        else:
            userid = request.args.get("userid")
        try:
            ObjectId(userid)
        except:
            userid = None
        if userid is not None:
            # response = DB.c_users.delete_by_id(userid)
            return jsonify({"Success": "Delete not working as yet"})
        else:
            abort(400, {'message': 'userid was either left blank or ill-formatted'})
    else:
        abort(401)
