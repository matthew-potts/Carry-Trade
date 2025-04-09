from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class PriceEntry:

    item: str = field(default_factory=str)
    entry: Dict[str, float] = field(default_factory=Dict)

    @property
    def open(self):
        return self.entry["o"]
    
    @property
    def high(self):
        return self.entry["h"]
    
    @property
    def low(self):
        return self.entry["l"]
    
    @property
    def close(self):
        return self.entry["c"]

    @property
    def volume(self):
        return self.entry["v"]
    
    @property
    def timestamp(self):
        return self.entry["t"]