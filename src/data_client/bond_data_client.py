from ibind import IbkrClient, ExternalBrokerError
from ibind.oauth.oauth1a import OAuth1aConfig
from os import environ as env
from src.data_client.base_data_client import BaseDataClient
from src.data_client.ibkr_connection import IBKRConnection
from src.logging.logger import project_logger
from typing import Dict, List

_LOGGER = project_logger(f"{__name__}")

class BondDataClient(BaseDataClient, IBKRConnection):

    def __init__(self, config_file: str):
        super().__init__(config_file)

    @property
    def asset_class(self):
        return "Bond"


