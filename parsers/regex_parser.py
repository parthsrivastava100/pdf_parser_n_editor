import re

from parsers.base import BaseParser


class RegexParser(BaseParser):
    def __init__(self, regex_patterns, keywords):
        super().__init__(keywords)
        
        self.regex_patterns = {re.compile(pattern, re.IGNORECASE): val for pattern, val in regex_patterns.items()}
    
    def detect_regex_matches(self, text):
        matches = []
        starts = set()
        
        for regex_pattern, conf in self.regex_patterns.items():
            for match in regex_pattern.finditer(text):
                start = match.start()
                data = match.group()
                end = start + len(data)
                if start not in starts:
                    matches.append({'start': start, 'end': end, 'data': data, 'confidence': conf})
                    starts.add(start)
        return matches
