from adsGenericFunctions.dbPgsql import dbPgsql
from adsGenericFunctions.logger import Logger
from adsGenericFunctions.global_config import set_timer

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
set_timer(True)

source = dbPgsql({'database': pg_dwh_db, 'user': pg_dwh_user, 'password': pg_dwh_pwd, 'port': pg_dwh_port,
                      'host': pg_dwh_host}, logger)
source.connect()

# Créons la table qui va recevoir nos données
source.sqlExec(''' DROP TABLE IF EXISTS demo_insert ''')
source.sqlExec('''
CREATE TABLE IF NOT EXISTS demo_insert (
    id SERIAL PRIMARY KEY,
    tenantname VARCHAR(255),
    fichier VARCHAR(255)
);
''')

# Insertion d'une ligne
resultat = source.insert('demo_insert', ['tenantname', 'fichier'], ['tenant_example', 'file_example'])
print(f"Resultat: {resultat}")

# Insertion de plusieurs lignes
rows_to_insert = [
    ('tenant1', 'file1.txt'),
    ('tenant2', 'file2.txt'),
    ('tenant3', 'file3.txt')
]
resultat = source.insertBulk('demo_insert', ['tenantname', 'fichier'], rows_to_insert)
print(f"Resultat: {resultat}")

# Lisons cette même table
data = source.sqlQuery(''' SELECT * FROM demo_insert ''')
print(list(data))

# Si une insertion rate, il y aura une erreur dans les logs en console, en base et en fichier
# mais aucune exception ne sera levée, c'est pourquoi il faut vérifier le retour
resultat = source.insert('demo_insert', ['tenantname', 'erreur'], ['tenant_example', 'file_example'])
print(f"Resultat: {resultat}")

logger.info("Fin de la démonstration.")