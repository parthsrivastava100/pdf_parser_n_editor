from constants.base import PII_ROUTING
from parsers.regex_parser import RegexParser
from parsers.util import combine_regex_and_context


class RoutingNumberParser(RegexParser):
    def __init__(self):
        regex_patterns = {
            r'\b((0[0-9])|(1[0-2])|(2[1-9])|(3[0-2])|(6[1-9])|(7[0-2])|80)([0-9]{7})\b': 0.95
        }
        keywords = {'routing': 0.8, 'bank': 0.7}
        super().__init__(regex_patterns, keywords)
        
        self.pii_type = PII_ROUTING
    
    def detect_pii(self, text, tagged_text):
        """
        Detect instances of PII in a given piece of text using a weighted combination of different methods.
        :param text: Raw text.
        :param tagged_text: POS and NE tagged tokens within the text.
        :return: Array of detected PII along with confidence metric.
        """
        
        regex_matches = self.detect_regex_matches(text)  # Return locations of regex matches
        valid_matches = [match for match in regex_matches if self.routing_validity_check(match.get('data'))]
        
        context_matches = self.detect_context_matches(text, tagged_text)  # Return locations of keyword matches
        
        return combine_regex_and_context(valid_matches, context_matches, self.pii_type)
    
    @staticmethod
    def routing_validity_check(routing_num) -> bool:
        """
        Verifies that the routing number matches the checksum formula and is valid.
        :param routing_num: Routing number (string)
        :return: Boolean representing validity of the routing number.
        """
        output = 3 * (int(routing_num[0]) + int(routing_num[3]) + int(routing_num[6])) + \
                 7 * (int(routing_num[1]) + int(routing_num[4]) + int(routing_num[7])) + \
                 int(routing_num[2]) + int(routing_num[5]) + int(routing_num[8])
        return output % 10 == 0
