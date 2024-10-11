from dataclasses import dataclass, asdict
import xml.etree.ElementTree as ET
import json

@dataclass
class BaseModel:
    def to_json(self) -> str:
        """Convert the instance to a JSON string."""
        return json.dumps(asdict(self), indent=4)
    
    def to_xml(self) -> str:
        """Convert the instance to an XML string."""
        root = ET.Element(self.__class__.__name__)
        self._to_xml_recursive(asdict(self), root)
        return ET.tostring(root, encoding='unicode', method='xml')
    
    def _to_xml_recursive(self, data, root):
        """Helper method to convert dictionary or list to XML recursively."""
        if isinstance(data, dict):
            for key, value in data.items():
                child = ET.SubElement(root, key)
                self._to_xml_recursive(value, child)
        elif isinstance(data, list):
            for item in data:
                item_elem = ET.SubElement(root, 'item')
                self._to_xml_recursive(item, item_elem)
        else:
            root.text = str(data)

    def to_dict(self) -> dict:
        """Convert the instance to a dictionary."""
        return asdict(self)
@dataclass
class EquityInfo(BaseModel):
    symbol: str
    nameOfCompany: str
    series: str
    dateOfListing: str
    isinNumber: str
    faceValue: int
    marketLot: int
    paidUpValue: int

@dataclass
class IndexInfo(BaseModel):
    key: str
    index: str
    indexSymbol: str
    last: float
    variation: float
    percentChange: float
    open: float
    high: float
    low: float
    previousClose: float
    yearHigh: float
    yearLow: float
    indicativeClose: int
    pe: str
    pb: str
    dy: str
    declines: str
    advances: str
    unchanged: str
    perChange365d: float
    date365dAgo: str
    chart365dPath: str
    date30dAgo: str
    perChange30d: float
    chart30dPath: str
    chartTodayPath: str
    previousDay: float
    oneWeekAgo: float
    oneMonthAgo: float
    oneYearAgo: float

@dataclass
class IndexStockWeightageInfo(BaseModel):
    symbol: str
    weight: float

@dataclass
class IndexSectorWeightageInfo(BaseModel):
    sector: str
    weight: float
    stocks: list[IndexStockWeightageInfo]


@dataclass
class IndexMoverStockInfo(BaseModel):
    symbol: str
    ltp: float
    change: float
    perChange: float
    high: float
    low: float
    sector: str
    indexPointChange: float
    indexPerChange: float