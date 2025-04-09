from typing import Dict, List
from dataclasses import dataclass, field
from src.data_client.price_entry import PriceEntry


@dataclass
class PriceHistory:
    # data: Dict[str, List[PriceEntry]] = field(default_factory=dict)

    def add_history(self, key: str, history: Dict[str, List[PriceEntry]]):
        if not self.item:
            self.data[key] = []
            [self.data[key].append(entry) for entry in history]
        if key not in self.data:
            raise KeyError(f"""A price history must have a unique key. Data for key {key} not allowed 
                           where {self.item} already specified.""")
        
    @property
    def item(self) -> str:
        return list(self.data.keys())[0]

    @property
    def data(self) -> List[PriceEntry]:
        return self.data.values()
    
