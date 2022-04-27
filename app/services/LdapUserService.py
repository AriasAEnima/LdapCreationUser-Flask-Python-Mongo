import ldap
import random
import string
import pandas
from passlib.hash import pbkdf2_sha256

from app import config
from app.services.sendEmails import sendEmail, getServer
    

def getRandomPassword():
    return ''.join(random.choice(string.ascii_letters) for i in range(12))
    

def aggregateMultipleUsersToLdif(startUid,dataframe: pandas.DataFrame):
    ldapconnection =connectToLdap()  
    clientEmail = getServer()
    for index, user in dataframe.iterrows():
        uid = user["email"].split("@")[0]
        newPassword = getRandomPassword()
        entry = []
        entry.extend([
            ('objectClass', [b"person", b"organizationalPerson", b"inetOrgPerson", b"posixAccount", b"top", b"shadowAccount"]),
            ('uid', uid.encode("utf-8")),
            ('cn', user["name"].encode("utf-8")),
            ('sn', user["surname"].encode("utf-8")),
            ('uidNumber', str(startUid).encode("utf-8")),
            ('gidNumber', b'1'),
            ('homeDirectory', b'/home'),
            ('mail', user["email"].encode("utf-8")),
            ('userPassword', newPassword.encode("utf-8"))
        ])
        startUid = startUid + 1
        final_user_dn = 'uid=' + uid + ',' + config.USER_DN_BASE
        try:
            ldapconnection.add_s(final_user_dn,entry)            
            dataframe.at[index,"username"] = uid
            dataframe.at[index,"password"] = pbkdf2_sha256.encrypt(newPassword)
            sendEmail(clientEmail,dataframe.loc[index,:],newPassword)
        except ldap.ALREADY_EXISTS as e:
            print(f"Ya se encuentra el usuario : {uid}")
    clientEmail.quit()
    ldapconnection.unbind_s()

     
def updatePassword(username, newpassword):
    ldapconnection = connectToLdap()
    final_user_dn = 'uid=' + username + ',' + config.USER_DN_BASE
    mod_attrs = [(ldap.MOD_REPLACE,"userPassword", newpassword.encode("utf-8"))]
    ldapconnection.modify_s(final_user_dn,mod_attrs)
    ldapconnection.unbind_s()


def connectToLdap():
    l = ldap.initialize(config.LDAP_ENDPOINT)
    #Bind to the server
    try:
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(config.BIND_DN, config.PASSWORD_ROOT) 
    except ldap.INVALID_CREDENTIALS:
        print("Your username or password is incorrect.")  
    except ldap.LDAPError as e:
        if type(e.message) == dict and e.message.has_key('desc'):
            print(e.message['desc'])
        else: 
            print(e)    
    return l

def createMultipleUsersLdap(dataframe: pandas.DataFrame):
    aggregateMultipleUsersToLdif(1,dataframe)
    print(f"Success process {len(dataframe)} users")
