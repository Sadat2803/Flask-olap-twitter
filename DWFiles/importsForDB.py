from eloquent import DatabaseManager, Model

configdb = {
        'mysql':{
            'driver': 'mysql',
            'host': 'localhost',
            'database': 'datawarehouse',
            'user': 'root',
            'password': '',
            'prefix':''
        }
    }

db = DatabaseManager(configdb)
Model.set_connection_resolver(db)
