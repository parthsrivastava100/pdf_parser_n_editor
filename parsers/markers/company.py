from constants.base import PII_COMPANY
from parsers.regex_parser import RegexParser
from parsers.util import combine_regex_and_context


class CompanyParser(RegexParser):
    def __init__(self):
        regex_patterns = {
            r'((?:\w[\ ]?)+): \$': 0.4,   #   'demo company - $' format 
             r'((?:\w[\ ]?)+)': 0.009,
                     
        }
        keywords = {'Issuer': 0.9, 'Investor': 0.9,'Stock':0.5,'Issuers':0.9,'Investors':0.9}
        super().__init__(regex_patterns,keywords)
        
        self.pii_type = PII_COMPANY
    
    def detect_pii(self, text, tagged_text):
        """
        Detect instances of PII in a given piece of text using a weighted combination of different methods.
        :param text: Raw text.
        :param tagged_text: POS and NE tagged tokens within the text.
        :return: Array of detected PII along with confidence metric.
        """
        regex_matches = self.detect_regex_matches(text)  # Return locations of regex matches
        context_matches = self.detect_context_matches(text, tagged_text)  # Return locations of keyword matches
        # TODO: Add pronoun detection
        
        return combine_regex_and_context(regex_matches, context_matches, self.pii_type)
