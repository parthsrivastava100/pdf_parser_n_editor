

from parsers.regex_parser import RegexParser
from parsers.util import combine_regex_and_context
from constants.base import PII_NAME




class NameParser(RegexParser):
    def __init__(self):
        self.pii_type = PII_NAME
        regex_patterns = {
         
            r'((?:\w[\ ]?)+)': 0.02
                     
        }
        keywords = {'name': 0.95, 'called': 0.6}
        super().__init__(regex_patterns,keywords)
    
    def detect_pii(self, text, tagged_text) -> list:
        regex_matches = self.detect_regex_matches(text)  # Return locations of regex matches
        context_matches = self.detect_context_matches(text, tagged_text)  # Return locations of keyword matches
        # TODO: Add pronoun detection
        
        return combine_regex_and_context(regex_matches, context_matches, self.pii_type)
