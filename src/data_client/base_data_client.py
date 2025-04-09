from pathlib import Path
import abc
import yaml
from typing import List, Dict
import sqlite3
from src.data_client.price_history import PriceHistory
from src.data_client.price_entry import PriceEntry
from src.logging.logger import project_logger

_LOGGER = project_logger(f"{__name__}")

class BaseDataClient(metaclass = abc.ABCMeta):

    def __init__(self, config_file: str):
        try:   
            with open(config_file) as stream:
                self.config = yaml.safe_load(stream)
                self.configure()
        except FileNotFoundError:
            print(f"Error: the config file {config_file} was not found.")
        except yaml.YAMLError as exc:
            print(f"Error occurred whilst loading YAML config file: {exc} ")
        
    def configure(self):
        """
        Configure the DataClient attributes from the loaded configuration.
        """
        for k, v in self.config.items():
            setattr(self, k, v)
        self.connect_to_db()
        self.connect()


    def connect_to_db(self):
        """
        """
        self.db_con = self._connect_to_db()
    
    def _connect_to_db(self):
        base_dir = Path(__file__).resolve().parents[1]
        con = sqlite3.connect(f"{base_dir}/{self.database}")
        con.isolation_level = None
        return con

    @abc.abstractmethod
    def connect(self) -> None:
        """
        Establish connection to upstream data provider specific to child class
        """
        pass

    @abc.abstractmethod
    def fetch(self, item: str) -> PriceHistory:
        """
        Fetches data based on item argument supplied
        """
        pass

    def write(self, history: List[PriceEntry]) -> None:
        for entry in history:
            try:
                query = self.build_write_query(entry)
                _LOGGER.info(f"Executing query: {query}")
                self.db_con.execute("BEGIN")
                self.db_con.execute(query)
                self.db_con.execute("COMMIT")
            except sqlite3.OperationalError as e:
                _LOGGER.error(f'Failed to add entry for {entry}. Exception: {e}')
                self.db_con.execute("ROLLBACK")

    @abc.abstractmethod
    def build_write_query(self, history: PriceEntry) -> str:
        pass
