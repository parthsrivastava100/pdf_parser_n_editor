from constants.base import PII_SSN
from parsers.regex_parser import RegexParser
from parsers.util import combine_regex_and_context


class SSNParser(RegexParser):
    def __init__(self):
        regex_patterns = {
            r'\b(?!000|666)[0-8][0-9]{2}-(?!00)[0-9]{2}-(?!0000)[0-9]{4}\b': 0.9,  # 123-45-6789
            r'\b(?!000|666)[0-8][0-9]{2}(?!00)[0-9]{2}(?!0000)[0-9]{4}\b': 0.25  # 123456789
        }
        keywords = {'social': 0.8, 'security': 0.8, 'ssn': 0.9, 'taxpayer': 0.8, 'identification': 0.3}
        super().__init__(regex_patterns, keywords)
        
        self.pii_type = PII_SSN
    
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
