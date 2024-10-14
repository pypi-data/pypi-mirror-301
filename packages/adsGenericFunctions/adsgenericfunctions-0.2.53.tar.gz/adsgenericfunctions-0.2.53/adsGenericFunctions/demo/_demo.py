import adsGenericFunctions as ads
from to_sort.env import *
import os

ads.set_timer(True) # active les timer

#--------------------------------------------------------------------------------------
#---------------------         DATA PIPELINE DB to DB         -------------------------
#--------------------------------------------------------------------------------------

def pipeline():
    pg_source=ads.dbPgsql({'database':pg_dwh_db
                            , 'user':pg_dwh_user
                            , 'password':pg_dwh_pwd
                            , 'port':pg_dwh_port
                            , 'host':pg_dwh_host})

    mssql_destination=ads.dbMssql({'database': mssql_dwh_db
                            , 'user':mssql_dwh_user
                            , 'password':mssql_dwh_pwd
                            , 'port':mssql_dwh_port
                            , 'host':mssql_dwh_host})


    mypipeline=ads.pipelineBulk({'db_source':pg_source
                         ,'query_source':'''SELECT tenantname, taille, unite, fichier FROM onyx_qs."diskcheck" LIMIT 10'''
                         ,'db_destination':mssql_destination
                         ,'table':'ONYX.diskcheck'
                         ,'cols':['tenantname', 'taille', 'unite', 'fichier']})


    mssql_destination=ads.dbMssql({'database': mssql_dwh_db
                            , 'user':mssql_dwh_user
                            , 'password':mssql_dwh_pwd
                            , 'port':mssql_dwh_port
                            , 'host':mssql_dwh_host})


    mypipeline=ads.pipeline({'db_source':pg_source
                         ,'query_source':'''SELECT tenantname, taille, unite, fichier FROM onyx_qs."diskcheck" LIMIT 10'''
                         ,'db_destination':mssql_destination
                         ,'table':'ONYX.diskcheck'
                         ,'cols':['tenantname', 'taille', 'unite', 'fichier']})

    mypipeline.run()

#--------------------------------------------------------------------------------------
#----------------------------         FICHIERS         --------------------------------
#--------------------------------------------------------------------------------------

def fichier():
    # lister un dossier
    os.listdir()

    # Copier un fichier
    #shutil.copy("trashcan.py", "../factory")

    #shutil.copy2() #--> conserve les metadata

    # Vérifier l'existance d'un fichier
    #os.path.isfile("")

pipeline()