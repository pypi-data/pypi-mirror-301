from adsGenericFunctions.logger import Logger
from adsGenericFunctions.dbPgsql import dbPgsql
from adsGenericFunctions.global_config import set_timer
from adsGenericFunctions.pipeline import pipeline_yield

from to_sort.env import *
import polars as pl
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

destination = dbPgsql({'database':pg_dwh_db
                    , 'user':pg_dwh_user
                    , 'password':pg_dwh_pwd
                    , 'port':pg_dwh_port
                    , 'host':pg_dwh_host}, logger)

# Créons la table de réception de nos données
destination.connect()
destination.sqlExec(''' DROP TABLE IF EXISTS demo_pipeline; ''')
destination.sqlExec('''
CREATE TABLE IF NOT EXISTS demo_pipeline (
    id SERIAL PRIMARY KEY,
    tenantname VARCHAR(255),
    taille FLOAT(8),
    unite VARCHAR(10),
    fichier VARCHAR(255)
);
''')

source = [
    ('ADS', 120.5, 'Mo', 'test1'),
    ('ADS', 130.7, 'Mo', 'test2'),
    ('ADS', "ERR", 'Mo', 'test3'),
    ('ADS', 100.0, 'Mo', 'test4')
]
df = pl.DataFrame(source, schema=['tenantname', 'taille', 'unite', 'fichier'], orient='row', strict=False)

logger.enable()
pipeline = pipeline_yield({
    'source': df,  # Donner le dataframe en source
    'db_destination': destination,
    'table': 'demo_pipeline',
    'cols': ['tenantname', 'taille', 'unite', 'fichier'],
    'batch_size': 2
}, logger)

rejects = pipeline.run()
print(f"{len(rejects)} rejet(s): {rejects}")

logger.info("Fin de la démonstration")