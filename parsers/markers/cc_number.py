import re

from constants.base import PII_CC_NUMBER
from parsers.regex_parser import RegexParser
from parsers.util import combine_regex_and_context


class CCNumberParser(RegexParser):
    def __init__(self):
        regex_patterns = {
            r'\b(^(4|5)\d{3}-?\d{4}-?\d{4}-?\d{4}|(4|5)\d{15})|(^(6011)-?\d{4}-?\d{4}-?\d{4}|(6011)-?\d{12})|(^((3\d{'
            r'3}))-\d{6}-\d{5}|^((3\d{14})))\b': 0.95,
            r'\b(\d{4}[- ]){3}\d{4}|\d{16}\b': 0.25  # 16 digit validation
        }
        keywords = {'credit': 0.8, 'card': 0.7, 'visa': 0.9, 'mastercard': 0.9, 'amex': 0.9, 'discover': 0.9}
        super().__init__(regex_patterns, keywords)
        
        self.pii_type = PII_CC_NUMBER
    
    def detect_pii(self, text, tagged_text):
        """
        Detect instances of PII in a given piece of text using a weighted combination of different methods.
        :param text: Raw text.
        :param tagged_text: POS and NE tagged tokens within the text.
        :return: Array of detected PII along with confidence metric.
        """
        
        regex_matches = self.detect_regex_matches(text)  # Return locations of regex matches
        valid_matches = [match for match in regex_matches if self.cc_number_validity_check(match.get('data'))]
        
        context_matches = self.detect_context_matches(text, tagged_text)  # Return locations of keyword matches
        
        return combine_regex_and_context(valid_matches, context_matches, self.pii_type)
    
    @staticmethod
    def cc_number_validity_check(cc_num) -> bool:
        """
        Verifies that the credit card number matches the checksum formula and is valid.
        :param cc_num: Credit card number (string).
        :return: Boolean representing validity of the credit card number.
        """
        cc_num = re.sub("[^0-9]", "", cc_num)  # Remove all non-digit characters
        checksum = cc_num[-1]
        cc_str = cc_num[-2::-1]  # Remove checksum character and reverse the number
        
        output = 0
        for i, char in enumerate(cc_str):
            tmp = int(char)
            # Multiply even digits by 2 and subtract 9 from any double digit results
            # Note: Checking for even instead of odd due to 0-based indexing
            if i % 2 == 0:
                tmp *= 2
                tmp -= 9 if tmp > 9 else 0
            
            output += tmp
        
        return (output + int(checksum)) % 10 == 0
