import re

from geotext import GeoText

from constants.base import PII_CITY
from core.util import format_pii_object
from parsers.base import BaseParser


class CityParser(BaseParser):
    def __init__(self):
        keywords = {}
        super().__init__(keywords=keywords)
    
    def detect_pii(self, text, tagged_text) -> list:
        output = []
        for city in GeoText(text).cities:
            for match in re.finditer(city, text):
                start = match.start()
                end = start + len(city)
                output.append(format_pii_object(start, end, PII_CITY, 0.9))
        
        return output
