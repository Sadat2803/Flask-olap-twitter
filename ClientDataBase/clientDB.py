import pandas as pd

from IntermediaryDB.covidStats import CovidStats


class ClientDB:

    def createClientDB(self):
        covidStatFile = pd.read_csv('covid_19.csv', sep=',', iterator=False, encoding='utf-8')


        for line in covidStatFile.to_numpy():
            covidStats = CovidStats()
            temp = line[3].split("/")
            y = temp[2]
            m = temp[0]
            d = temp[1]
            if len(m)==1:
                m = '0'+m
            if len(d)==1:
                d = '0'+d
            dateCode = "".join([y,m,d])
            date = "-".join([temp[2],temp[0],temp[1]])
            row = [line[0].lower(), date, dateCode, line[4], line[5], line[6]]
            print(row)
            covidStats.insert(row)
        print("insertion complete")

if __name__=="__main__":
    db = ClientDB()
    db.createClientDB()
