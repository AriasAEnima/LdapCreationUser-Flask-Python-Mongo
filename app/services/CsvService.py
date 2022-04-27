import pandas as pd

def readCSV(csvFile):
    df = pd.read_csv(csvFile.stream,header=0)
    df['password']=''
    df['username']=''
    df['mustChangePassword']= True
    return df