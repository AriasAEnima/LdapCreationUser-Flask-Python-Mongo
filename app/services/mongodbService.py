from pymongo import MongoClient
from app import config
import pandas

def initClient():
    client = MongoClient(f"mongodb+srv://{config.USER_MONGO}:{config.PASSWORD_MONGO}@ldaploginbackup.vxj50.mongodb.net/ldapUsers?retryWrites=true&w=majority")
    
    return client

def saveUsers(dataframe: pandas.DataFrame):
    usersConnection = initClient()
    usersConnection['ldapUsers']['users'].insert_many(dataframe.to_dict('records'))
    usersConnection.close()