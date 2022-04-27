import os

PASSWORD_ROOT = os.getenv('PASSWORD_ROOT',"secret")
USER_DN_BASE = os.getenv('USER_DN_BASE',"dc=maxcrc,dc=com")
BIND_DN = os.getenv("BIND_DN","cn=Manager,dc=maxcrc,dc=com")
LDAP_ENDPOINT = os.getenv("LDAP_ENDPOINT","ldap://localhost:389")
PASSWORD_ADMIN_TEST_EMAIL = os.getenv("PASSWORD_ADMIN_TEST_EMAIL")
USER_MONGO = os.getenv("USER_MONGO","ldapAdmin")
PASSWORD_MONGO = os.getenv("PASSWORD_MONGO")