from adsGenericFunctions.logger import Logger
from adsGenericFunctions.dbPgsql import dbPgsql
from adsGenericFunctions.global_config import set_timer
from adsGenericFunctions.pipeline import pipeline

from to_sort.env import *
import logging

logger_connection = dbPgsql({'database': pg_dwh_db
                          , 'user': pg_dwh_user
                          , 'password': pg_dwh_pwd
                          , 'port': pg_dwh_port
                          , 'host': pg_dwh_host},
                      None)
logger_connection.connect()
logger = Logger(logger_connection, logging.INFO, "AdsLogger", "LOGS", "LOGS_details")
logger.info("Début de la démonstration...")
logger.disable()
set_timer(True)

# Cette fois, on va déclarer plusieurs destinations
destination_1 = {
    'db': dbPgsql({'database':pg_dwh_db, 'user':pg_dwh_user, 'password':pg_dwh_pwd, 'port':pg_dwh_port
                    , 'host':pg_dwh_host}, logger),
    'table': 'demo_pipeline',
    'cols': ['tenantname', 'taille', 'unite', 'fichier']
}
destination_2 = {
    'db': dbPgsql({'database':pg_dwh_db, 'user':pg_dwh_user, 'password':pg_dwh_pwd, 'port':pg_dwh_port
                    , 'host':pg_dwh_host}, logger),
    'table': 'demo_pipeline',
    'cols': ['tenantname', 'taille', 'unite', 'fichier']
}

# Créons la table de réception de nos données
destination_1['db'].connect()
destination_1['db'].sqlExec(''' DROP TABLE IF EXISTS demo_pipeline; ''')
destination_1['db'].sqlExec('''
CREATE TABLE IF NOT EXISTS demo_pipeline (
    id SERIAL PRIMARY KEY,
    tenantname VARCHAR(255),
    taille FLOAT(8),
    unite VARCHAR(10),
    fichier VARCHAR(255)
);
''')

# Notre source sera ce tableau
source = [
    ('ADS', "ERR", 'Mo', 'test1'),
    ('ADS', 130.7, 'Mo', 'test2'),
    ('ADS', "ERR", 'Mo', 'test3'),
    ('ADS', 100.0, 'Mo', 'test4')
]

logger.enable()
pipe = pipeline({
    'tableau': source,
    'db_destinations': destination_1,
    'batch_size': 2
}, logger)

rejects = pipe.run()
print(f"{len(rejects)} rejet(s): {rejects}")

logger.info("Fin de la démonstration")