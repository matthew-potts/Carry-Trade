from ibind import ExternalBrokerError
from src.data_client.base_data_client import BaseDataClient
from src.data_client.price_entry import PriceEntry
from src.data_client.ibkr_connection import IBKRConnection
from src.logging.logger import project_logger
from typing import Dict, List


_LOGGER = project_logger(f"{__name__}")

class FXDataClient(BaseDataClient, IBKRConnection):

    def __init__(self, config_file: str):
        super().__init__(config_file)

    def fetch(self, item: str) -> Dict[str, List[PriceEntry]]:
        try:    
            _LOGGER.info(f"Fetching price history for item {item}")
            conid = self.client.search_contract_by_symbol(item).data[0]['conid']
            history = self.client.marketdata_history_by_conid(conid=conid, period='1y', bar='1d', outside_rth=True).data['data']
            return [PriceEntry(item = item, entry = x) for x in history]
        except ExternalBrokerError as ex:
            _LOGGER.error(f'Error: Unable to retrieve price history for currency {item}: {ex}')        
        
    
    def build_write_query(self, entry: PriceEntry) -> str:
        query = f"""INSERT INTO currency (curr, open, close, high, low, volume, timestamp)
                VALUES (
                    '{entry.item}', 
                    '{entry.open}', 
                    '{entry.close}', 
                    '{entry.high}', 
                    '{entry.low}',
                    '{entry.volume}', 
                    '{entry.timestamp}'
                )"""
        return query
        