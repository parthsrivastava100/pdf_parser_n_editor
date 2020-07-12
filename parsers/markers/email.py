from constants.base import PII_EMAIL
from parsers.regex_parser import RegexParser
from parsers.util import combine_regex_and_context


class EmailParser(RegexParser):
    def __init__(self):
        regex_patterns = {
            r'\b\b([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,'
            r'4}|[0-9]{1,3})(\]?)\b\b': 0.9
        }
        keywords = {'e-mail': 1.0, 'email': 1.0}
        super().__init__(regex_patterns, keywords)
        
        self.pii_type = PII_EMAIL
    
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
