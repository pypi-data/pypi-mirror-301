import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
import psycopg2
import os
import uuid
import sys

from .dbPgsql import dbPgsql
from .dbMssql import dbMssql


class CustomFormatter(logging.Formatter):
    grey = "\x1b[37m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.format)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger:
    def __init__(self, connection, logLevel=logging.INFO, logger_name="AdsLogger", table_log_name="LOGS", table_log_details_name="LOGS_details"):
        self.logLevel = logLevel
        self.logger = self.__setup_logger(logger_name)
        self.connection = connection
        self.db_logging_enabled = True
        self.table_log_name = table_log_name
        self.table_log_details_name = table_log_details_name

    def __setup_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(self.logLevel)

        # Ecriture dans un fichier
        file_handler = TimedRotatingFileHandler(filename="log.txt", when='D', interval=1, backupCount=10)
        file_handler.setLevel(self.logLevel)

        # Ecriture dans la console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.logLevel)

        # Formatter pour le fichier (sans couleurs)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # Formatter personnalisé pour la console (avec couleurs)
        console_handler.setFormatter(CustomFormatter())

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def _get_connection(self):
        if isinstance(self.connection, (dbPgsql, dbMssql)):
            return self.connection.connection
        return self.connection

    def _create_logs_tables_if_not_exists(self):
        if not self.connection or not self.db_logging_enabled:
            return
        create_logs_table_query = f"""
                    CREATE TABLE IF NOT EXISTS {self.table_log_name} (
                        start_time TIMESTAMP PRIMARY KEY,
                        end_time TIMESTAMP,
                        job_key UUID,
                        full_path TEXT,
                        status VARCHAR(50),
                        message TEXT
                    );
                """
        create_logs_details_table_query = f"""
                    CREATE TABLE IF NOT EXISTS {self.table_log_details_name} (
                        date TIMESTAMP PRIMARY KEY,
                        job_key UUID,
                        log_level VARCHAR(20),
                        message TEXT
                    );
                """
        try:
            with self._get_connection().cursor() as cursor:
                cursor.execute(create_logs_table_query)
                cursor.execute(create_logs_details_table_query)
                self._get_connection().commit()
                self.info(f"Tables {self.table_log_name} et {self.table_log_details_name} vérifiées/créées.")
        except Exception as e:
            self.error(f"Erreur lors de la création des tables de logs: {e}")

    def log_to_db(self, start_time: datetime, end_time: datetime, status: str, message: str):
        """Insère un log dans la table principale et dans la table des détails."""
        if not self.connection or not self.db_logging_enabled:
            return
        job_key = uuid.uuid4()
        full_path = os.path.relpath(sys.argv[0], start=os.path.dirname(os.getcwd()))
        try:
            self._insert_logs_tables(job_key, start_time, end_time, full_path, status, message)
        except psycopg2.errors.UndefinedTable:
            self.error(f"Table(s) de logs non trouvée, tentative de création...")
            self._get_connection().rollback()
            self._create_logs_tables_if_not_exists()
            self._insert_logs_tables(job_key, start_time, end_time, full_path, status, message)
        except Exception as e:
            self.error(f"Erreur lors des insertions dans les table de logs: {e}")
            self._get_connection().rollback()
            raise

    def _insert_logs_tables(self, job_key: uuid, start_time: datetime, end_time: datetime, full_path: str, status: str,
                            message: str):
        if not self.connection or not self.db_logging_enabled:
            return
        with self._get_connection().cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO {self.table_log_name} (job_key, start_time, end_time, full_path, status, message)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (str(job_key), start_time, end_time, full_path, status, message)
            )
            cursor.execute(
                f"""
                INSERT INTO {self.table_log_details_name} (job_key, date, log_level, message)
                VALUES (%s, %s, %s, %s)
                """,
                (str(job_key), datetime.now(), self.logLevel, message)
            )
            self._get_connection().commit()
            self.info(f"Logs inséré dans les tables {self.table_log_name} et {self.table_log_details_name}.")

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def enable(self, logLevel=logging.INFO):
        self.logger.setLevel(logLevel)
        self.db_logging_enabled = True

    def disable(self):
        self.logger.setLevel(logging.CRITICAL)
        self.db_logging_enabled = False
