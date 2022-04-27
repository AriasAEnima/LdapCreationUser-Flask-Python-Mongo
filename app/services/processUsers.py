from app.services.LdapUserService import createMultipleUsersLdap
from app.services.CsvService import readCSV
from app.services.mongodbService import saveUsers


def processUsers(csvFile):
    dataframe = readCSV(csvFile)
    createMultipleUsersLdap(dataframe)
    dataframe.info()
    print(dataframe.iloc[0])
    saveUsers(dataframe)