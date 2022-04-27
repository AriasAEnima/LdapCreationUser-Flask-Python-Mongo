from app.services.mongodbService import initClient
from passlib.hash import pbkdf2_sha256
from flask import jsonify, redirect, session, request
from app.services.LdapUserService import updatePassword

class User:
    def start_session(self,user):
        session['logged_in'] = True
        del user['_id']
        session['user'] = user
        return jsonify(user), 200

    def login(self):        
        user = initClient()['ldapUsers']['users'].find_one({
            "username": request.form.get('username')
            })
        print(user)      
        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        return jsonify({ "error": "Invalid login credentials" }), 401
    
    def changePassword(self):
        query = {
            "username": session['user']['username']
        }
        user = initClient()['ldapUsers']['users'].find_one(query)

        if user and pbkdf2_sha256.verify(request.form.get('oldpassword'), user['password']) and request.form.get('newpassword') \
            == request.form.get('repeatpassword') and request.form.get('oldpassword')!=request.form.get('newpassword'):
            mongoClient =  initClient()
            newvalues = { "$set": 
                            { 
                                "password":pbkdf2_sha256.encrypt(request.form.get('newpassword')),
                                "mustChangePassword": False
                            } 
                        }
            mongoClient['ldapUsers']['users'].update_one(query,newvalues)
            user = mongoClient['ldapUsers']['users'].find_one(query)
            updatePassword(user["username"],request.form.get('newpassword'))
            mongoClient.close()
            return self.start_session(user)            
        return jsonify({ "error": "Invalid password credentials" }), 401    
    
    def signout(self):
        session.clear()
        return redirect('/')