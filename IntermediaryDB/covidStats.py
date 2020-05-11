from eloquent import DatabaseManager, Model

config = {
        'mysql':{
            'driver': 'mysql',
            'host': 'localhost',
            'database': 'interdb',
            'user': 'root',
            'password': '',
            'prefix':''
        }
    }

db = DatabaseManager(config)
Model.set_connection_resolver(db)

class CovidStats(Model):
    __fillable__ = ['country','date','dateCode','confirmed','deaths','recovered']
    __timestamps__ = False
    __table__ = "covidstats"

    def insert(self,row):
        self.country = row[0]
        self.date = row[1]
        self.dateCode = row[2]
        self.confirmed = row[3]
        self.deaths = row[4]
        self.recovered = row[5]
        self.save()
