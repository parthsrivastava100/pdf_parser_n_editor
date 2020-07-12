from constants.base import PII_GENDER
from parsers.regex_parser import RegexParser
from parsers.util import combine_regex_and_context


class GenderParser(RegexParser):
    def __init__(self):
        regex_patterns = {
            r'\b(?:male|female|man|woman|men|women|boy|girl|girls)\b': 0.9,
            r'\b(?:m|M|f|F|guy|guys)\b': 0.3
        }
        keywords = {'gender': 0.95, 'sex': 0.7}
        super().__init__(regex_patterns, keywords)
        
        self.pii_type = PII_GENDER
    
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
