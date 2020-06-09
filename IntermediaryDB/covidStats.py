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
    __fillable__ = ['country','countryCode','date','dateCode','confirmed','deaths','recovered']
    __timestamps__ = False
    __table__ = "covidstats"

    def insert(self,row):
        self.country = row[0]
        self.countryCode = row[1]
        self.date = row[2]
        self.dateCode = row[3]
        self.confirmed = row[4]
        self.deaths = row[5]
        self.recovered = row[6]
        self.save()
