import re
from loguru import logger
from constants.base import PII_COUNTRY
from core.util import capitalize_first_letters, format_pii_object
from parsers.base import BaseParser
from iso3166 import countries
from fuzzywuzzy import process


def diff_token_penalty(string1, string2):
    total_cap_penalty = 20
    penalty_constant = 5
    total_diff = len([i for i in range(len(string1)) if string1[i] != string2[i]])
    # Have base penalty low for Capitalization and all lower or uppercase
    if (total_diff == 1 and string1[0] != string2[0]) or total_diff == len(string1):
        penalty = penalty_constant
    else:
        penalty = total_diff * penalty_constant
    return abs(total_cap_penalty - penalty)


def iter_match_text(token_name, text, confidence):
    return [
        format_pii_object(
            start=index.start(),
            end=index.end(),
            pii_type=PII_COUNTRY,
            confidence=confidence,
        )
        for index in re.finditer(token_name, text)
    ]


class CountryParser(BaseParser):
    def __init__(self):
        keywords = {
            "live": 0.95,
            "from": 0.8,
            "home": 0.6,
            "country": 0.95,
            "nation": 0.95,
        }
        custom_countries = ["Russia"]
        self.countries = []
        self.country_two_abb = []
        self.country_three_abb = []
        super().__init__(keywords=keywords)
        for c in countries:
            self.countries.append(c.name)
            self.country_two_abb.append(c.alpha2)
            self.country_three_abb.append(c.alpha3)

        self.countries.extend(custom_countries)

    def detect_pii(self, text, tagged_text) -> list:
        output = []
        for sentence in tagged_text:
            for token in sentence:
                token_name = token[0]
                if token_name in self.country_two_abb:
                    output.extend(iter_match_text(token_name, text, 0.90))
                elif (
                    token[1] in ["NN", "NNS", "NNP", "NNPS", "JJ"]
                    and len(token_name) > 3
                ):
                    confidence_score = 0
                    match_with_score = process.extractOne(token_name, self.countries)
                    score = match_with_score[1]
                    match_token = match_with_score[0]
                    if (
                        score >= 80
                        and len(match_token) < len(token_name) * 1.30
                        and len(match_token) > len(token_name) * 0.70
                    ):
                        confidence_score = score * 0.8
                        if score == 100:
                            confidence_score += diff_token_penalty(
                                match_token, token_name
                            )
                        output.extend(
                            iter_match_text(token_name, text, (confidence_score / 100))
                        )
        return output
