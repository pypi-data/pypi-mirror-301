from .timer import timer
from .logger import Logger
import polars as pl

class pipeline:
    def __init__(self, dictionnary: dict, logger: Logger):
        self.logger = logger
        self.__db_source = dictionnary.get('db_source')
        self.__query_source = dictionnary.get('query_source')
        self.__tableau = dictionnary.get('tableau')
        self.__batch_size = dictionnary.get('batch_size', 10_000)
        db_destinations = dictionnary.get('db_destinations')
        if isinstance(db_destinations, list):
            self.__db_destinations = db_destinations
        else:
            self.__db_destinations = [db_destinations]

    def _data_generator(self, cols):
        self.logger.info("Chargement des données depuis la source...")
        if self.__tableau is not None and self.__db_source is not None:
            msg = "Deux sources de données différentes sont définies, veuillez n'en choisir qu'une."
            self.logger.error(msg)
            raise ValueError(msg)
        if self.__tableau is not None and len(self.__tableau) > 0:
            for start in range(0, len(self.__tableau), self.__batch_size):
                batch = self.__tableau[start:start + self.__batch_size]
                yield pl.DataFrame(batch, orient='row', schema=cols, strict=False)
        elif self.__db_source and self.__query_source:
            self.logger.disable()
            self.__db_source.connect()
            self.logger.enable()
            for batch in self.__db_source.sqlQuery(self.__query_source):
                yield pl.DataFrame(batch, orient='row', schema=cols, strict=False)
        else:
            raise ValueError("Source de données non supportée.")

    @timer
    def run(self):
        rejects = []
        try:
            for destination in self.__db_destinations:
                self.logger.disable()
                destination['db'].connect()
                self.logger.enable()
                self.logger.info(f"Connexion à {destination.get('name', 'la base de donnée')} réussie.")
                for batch_df in self._data_generator(destination.get("cols")):
                    insert_result = destination.get('db').insertBulk(
                        table=destination.get('table'),
                        cols=destination.get('cols'),
                        rows=batch_df.rows()
                    )

                    if insert_result[0]=="ERROR":
                        rejects.append((destination.get('name'), insert_result, batch_df.rows()))
        except Exception as e:
            self.logger.enable()
            self.logger.error(f"Échec de l'exécution du pipeline: {e}")
            raise
        return rejects
