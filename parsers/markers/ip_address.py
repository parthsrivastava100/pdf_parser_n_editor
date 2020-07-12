from constants.base import PII_IP
from parsers.regex_parser import RegexParser
from parsers.util import combine_regex_and_context

class IPAddressParser(RegexParser):
    def __init__(self):
        regex_patterns = {
            r'\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b' : 0.9,
            r'\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?):\d{4}\b' : 0.9
        }
        keywords = {'ip': 0.9 ,'ipv4': 0.9 , 'address': 0.8, 'from': 0.7, 'by': 0.6, 'host': 0.9, 'root': 0.8}
        super().__init__(regex_patterns, keywords)
        
        self.pii_type = PII_IP
        
    def detect_pii(self, text , tagged_text):
        """
        Detect instances of PII in a given piece of text using a weighted combination of different methods.
        :param text: Raw text.
        :param tagged_text: POS and NE tagged tokens within the text.
        :return: Array of detected PII along with confidence metric.
        """
        
        regex_matches = self.detect_regex_matches(text)  # Return locations of regex matches
        context_matches = self.detect_context_matches(text, tagged_text)  # Return locations of keyword matches
        
        return combine_regex_and_context(regex_matches, context_matches, self.pii_type)
