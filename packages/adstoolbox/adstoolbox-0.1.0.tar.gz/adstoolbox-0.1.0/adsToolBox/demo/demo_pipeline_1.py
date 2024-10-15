from adsToolBox.logger import Logger
from adsToolBox.dbPgsql import dbPgsql
from adsToolBox.global_config import set_timer
from adsToolBox.pipeline import pipeline

from to_sort.env import *
import logging

logger_connection = dbPgsql({'database': pg_dwh_db
                          , 'user': pg_dwh_user
                          , 'password': pg_dwh_pwd
                          , 'port': pg_dwh_port
                          , 'host': pg_dwh_host},
                      None, 10_000)
logger_connection.connect()
logger = Logger(logger_connection, logging.INFO, "AdsLogger", "LOGS", "LOGS_details")
logger.info("Début de la démonstration...")
logger.disable()
set_timer(True)

# Déclarons une source base de données
source = dbPgsql({'database':pg_dwh_db
                    , 'user':pg_dwh_user
                    , 'password':pg_dwh_pwd
                    , 'port':pg_dwh_port
                    , 'host':pg_dwh_host}, logger, batch_size=1)

# Déclarer une destination, c'est un peu plus complexe
destination = {
    'name': 'test',
    'db': dbPgsql({'database':pg_dwh_db, 'user':pg_dwh_user, 'password':pg_dwh_pwd, 'port':pg_dwh_port
                    , 'host':pg_dwh_host}, logger),
    'table': 'demo_pipeline',
    'cols': ['tenantname', 'taille', 'unite', 'fichier']
}

# Créons la table de réception de nos données
destination['db'].connect()
destination['db'].sqlExec(''' DROP TABLE IF EXISTS demo_pipeline; ''')
destination['db'].sqlExec('''
CREATE TABLE IF NOT EXISTS demo_pipeline (
    id SERIAL PRIMARY KEY,
    tenantname VARCHAR(255),
    taille FLOAT(8),
    unite VARCHAR(10),
    fichier VARCHAR(255)
);
''')

# Voici la requête pour la source
query = '''
SELECT tenantname, taille, unite, fichier
FROM onyx_qs."diskcheck" LIMIT 5
'''
logger.enable()

# Premier pipeline
pipeline_1 = pipeline({
    'db_source': source, # La source du pipeline
    'query_source': query, # La requête qui sera exécutée sur cette source
    'db_destinations': destination, # La destination du pipeline
    'batch_size': 1
}, logger)

rejects = pipeline_1.run() # pipeline.run() renvoie les rejets du pipeline, ce sera une liste vide s'il
# n'y en a pas
print(f"{len(rejects)} rejets : {rejects}")

# Un batch_size à 1, ce insère les lignes une par une, un batch_size plus grand implique un run plus rapide
# pour le même nombre de lignes, batch_size est à 10 000 par défaut
# Second pipeline
source = dbPgsql({'database':pg_dwh_db
                    , 'user':pg_dwh_user
                    , 'password':pg_dwh_pwd
                    , 'port':pg_dwh_port
                    , 'host':pg_dwh_host}, logger)

pipeline_2 = pipeline({
    'db_source': source, # La source du pipeline
    'query_source': query, # La requête qui sera exécutée sur cette source
    'db_destinations': destination # La destination du pipeline
}, logger)

rejects = pipeline_2.run()
print(f"{len(rejects)} rejets : {rejects}")


logger.info("Fin de la démonstration")