from ibind import ExternalBrokerError
from pathlib import Path
from abc import ABC, abstractmethod, ABCMeta
import yaml
from typing import List, Dict
import sqlite3
from ibind.oauth.oauth1a import OAuth1aConfig
from src.data_client.price_history import PriceHistory
from src.data_client.price_entry import PriceEntry
from src.logging.logger import project_logger
from src.data_client.ibkr_connection import IbkrClient
from os import environ as env

_LOGGER = project_logger(f"{__name__}")

class BaseDataClient(metaclass = ABCMeta):

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

    def connect(self) -> None:
        _LOGGER.info("Connecting IBKR client")
        self.client = IbkrClient(
            use_oauth=True,
            oauth_config=OAuth1aConfig(
                access_token=env['IBIND_OAUTH1A_ACCESS_TOKEN'],
                access_token_secret=env['IBIND_OAUTH1A_ACCESS_TOKEN_SECRET'],
                consumer_key=env['IBIND_OAUTH1A_CONSUMER_KEY'],
                dh_prime=env['IBIND_OAUTH1A_DH_PRIME'],
                encryption_key_fp=env['IBIND_OAUTH1A_ENCRYPTION_KEY_FP'],
                signature_key_fp=env['IBIND_OAUTH1A_SIGNATURE_KEY_FP'],
        )
    )

    def fetch(self, item: str, period: str, bar: str = '1d') -> Dict[str, List[PriceEntry]]:
        try:    
            _LOGGER.info(f"Fetching price history for item {item}")
            conid = self.client.search_contract_by_symbol(item).data[0]['conid']
            history = self.client.marketdata_history_by_conid(conid=conid, period=period, bar=bar, outside_rth=True).data['data']
            return [PriceEntry(item = item, entry = x) for x in history]
        except ExternalBrokerError as ex:
            _LOGGER.error(f'Error: Unable to retrieve price history for currency {item}: {ex}')        
        
    def build_write_query(self, entry: PriceEntry) -> str:
        query = f"""INSERT INTO price (class, item, open, close, high, low, volume, timestamp)
                VALUES (
                    '{self.asset_class}',
                    '{entry.item}', 
                    '{entry.open}', 
                    '{entry.close}', 
                    '{entry.high}', 
                    '{entry.low}',
                    '{entry.volume}', 
                    '{entry.timestamp}'
                )"""
        return query
    
    def write(self, history: List[PriceEntry]) -> None:
        
        if history is not None:
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
                    break

    @property
    @abstractmethod
    def asset_class(self):
        """
        The asset class for which the data processes data.
        Appears as an entry in the 'class' column of the 'price' table.
        """
        pass
