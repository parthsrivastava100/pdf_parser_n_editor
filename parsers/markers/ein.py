from constants.base import PII_EIN
from parsers.regex_parser import RegexParser
from parsers.util import combine_regex_and_context


class EINParser(RegexParser):
    def __init__(self):
        regex_patterns = {
            r'\b\d{2}-\d{7}\b': 0.93,  # 12-3456789
            r'\b\d{9}\b': 0.25  # 123456789
        }
        keywords = {'employee': 0.7, 'identification': 0.3, 'ein': 0.9, 'tax': 0.4, 'taxpayer': 0.3}
        super().__init__(regex_patterns, keywords)
        
        self.pii_type = PII_EIN
    
    def detect_pii(self, text, tagged_text):
        """
        Detect instances of PII in a given piece of text using a weighted combination of different methods.
        :param text: Raw text.
        :param tagged_text: POS and NE tagged tokens within the text.
        :return: Array of detected PII along with confidence metric.
        """
        
        regex_matches = self.detect_regex_matches(text)  # Return locations of regex matches
        context_matches = self.detect_context_matches(text, tagged_text)  # Return locations of keyword matches
        
        return combine_regex_and_context(regex_matches, context_matches, self.pii_type)
