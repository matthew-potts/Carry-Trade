from ibind import ExternalBrokerError
from src.data_client.base_data_client import BaseDataClient
from src.data_client.price_entry import PriceEntry
from src.data_client.ibkr_connection import IBKRConnection
from src.logging.logger import project_logger
from typing import Dict, List


_LOGGER = project_logger(f"{__name__}")

class FXDataClient(BaseDataClient):

    def __init__(self, config_file: str):
        super().__init__(config_file)

    @property
    def asset_class(self):
        return "FX"