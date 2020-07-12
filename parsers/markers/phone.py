from constants.base import PII_USA_PHONE
from parsers.regex_parser import RegexParser
from parsers.util import combine_regex_and_context


class USAPhoneParser(RegexParser):
    def __init__(self):
        regex_patterns = {
            r'\(\d{3}\)\s\d{3}-\d{4}': 0.9,  # (123) 456-7890_
            r'\b(\+1(\s|-))?\d{3}(-|\s)?\d{3}-?\d{4}\b': 0.7,  # +1-123-456-7890
            r'\b(\d{3}(\s|-)?\d{3}(\s|-)?\d{4})\b':0.7  #123 456 7890
        }
        keywords = {'telephone': 0.9, 'number': 0.7, 'phone': 0.9, 'text': 0.8, 'mms': 0.9, 'sms': 0.9, 'message': 0.4}
        super().__init__(regex_patterns, keywords)
        
        self.pii_type = PII_USA_PHONE
    
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
