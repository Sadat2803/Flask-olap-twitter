from eloquent import DatabaseManager, Model

config = {
        'mysql':{
            'driver': 'mysql',
            'host': 'localhost',
            'database': 'tweetsdatawarehouse',
            'user': 'root',
            'password': '',
            'prefix':''
        }
    }

db = DatabaseManager(config)
Model.set_connection_resolver(db)
