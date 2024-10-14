from .timer import timer
from .logger import Logger
import polars as pl

class pipeline_yield:
    def __init__(self, dictionnary: dict, logger: Logger):
        self.logger = logger
        self.__source = dictionnary.get('source')
        self.__db_destination = dictionnary.get('db_destination')
        self.__table = dictionnary.get('table')
        self.__cols = dictionnary.get('cols')
        self.__batch_size = dictionnary.get('batch_size', 1)

    def _data_generator(self, df: pl.DataFrame):
        for start in range(0, df.shape[0], self.__batch_size):
            end = start + self.__batch_size
            yield df[start:end].rows()

    @timer
    def run(self):
        res = []
        try:
            if not isinstance(self.__source, pl.DataFrame):
                raise ValueError("Les données fournies ne sont pas un DataFrame polars.")
            self.logger.enable()
            self.__db_destination.connect()
            self.logger.info(f"{self.__source.shape[0]} lignes récupérées.")
            for batch in self._data_generator(self.__source):
                insert_result = self.__db_destination.insertBulk(
                    table=self.__table,
                    cols=self.__cols,
                    rows=list(batch)
                )
                if insert_result[0] == "ERROR":
                    res.append((insert_result, batch))
        except Exception as e:
            self.logger.error(f"Échec de l'exécution du pipeline: {e}")
            raise
        return res

class pipeline:
    def __init__(self, dictionnary: dict, logger: Logger):
        self.logger = logger
        self.__db_source = dictionnary.get('db_source')
        self.__query_source = dictionnary.get('query_source')
        self.__tableau = dictionnary.get('tableau')
        self.__batch_size = dictionnary.get('batch_size', 1)
        db_destinations = dictionnary.get('db_destinations')
        if isinstance(db_destinations, list):
            self.__db_destinations = db_destinations
        else:
            self.__db_destinations = [db_destinations]

    @timer
    def _load_data(self):
        self.logger.info("Chargement des données depuis la source...")
        self.logger.disable()
        if self.__tableau is not None and len(self.__tableau) > 0:
            res = self.__tableau
        elif self.__db_source and self.__query_source:
            self.__db_source.connect()
            res = list(self.__db_source.sqlQuery(self.__query_source))
        else:
            raise ValueError("Source de données non supportée.")
        return pl.DataFrame(res, orient='row', strict=False)

    @timer
    def run(self):
        rejects = []
        try:
            df = self._load_data()
            for destination in self.__db_destinations:
                destination['db'].connect()
            self.logger.enable()
            self.logger.info(
                f"Connexion(s) établie(s) avec {len(self.__db_destinations)} base(s) de données destination.")
            self.logger.info(f"{df.shape[0]} lignes récupérées.")
            for start in range(0, df.shape[0], self.__batch_size):
                end = start + self.__batch_size
                batch = df[start:end].rows()
                for destination in self.__db_destinations:
                    db = destination['db']
                    table = destination['table']
                    cols = destination['cols']
                    insert_result = db.insertBulk(
                        table=table,
                        cols=cols,
                        rows=list(batch)
                    )
                    if insert_result[0] == "ERROR":
                        rejects.append((destination, insert_result, batch))
        except Exception as e:
            self.logger.error(f"Échec de l'exécution du pipeline: {e}")
            raise
        return rejects
