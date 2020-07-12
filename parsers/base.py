import abc

from fuzzywuzzy import fuzz
from loguru import logger


class BaseParser:
    """
    BaseParser implements functionality common to every PII marker. Each marker will use contextual information
    to determine a confidence score for the prediction using keywords and fuzzy matching.
    """
    
    def __init__(self, keywords):
        self.keywords = keywords
    
    def detect_context_matches(self, text, text_tagged, min_thresh=0.3) -> list:
        """
        Returns matches of the parser's keywords in the selected text.
        :param text: Plaintext input
        :param text_tagged: Tagged and tokenized text input
        :param min_thresh: Minimum match % threshold to be considered a contextual match
        :return: List of contextual matches for the given parser
        """
        
        chunks = []
        
        new_chunk = ""
        for sentence in text_tagged:
            for token, pos, ne, iob in sentence:
                if iob.startswith('B'):  # New chunk is beginning, save the old one
                    if new_chunk != "":
                        chunks.append(new_chunk)
                    new_chunk = token
                elif iob.startswith('I'):  # Chunk is continuing
                    new_chunk += f" {token}"
                elif iob.startswith('O'):  # Chunk ended, reset
                    chunks.append(new_chunk)
                    new_chunk = ""
        
        chunks.append(new_chunk)  # Add any remainder to the end of the chunk array
        logger.debug(f'Chunks: {chunks}')
        
        context_matches = []
        for chunk in chunks:
            tokenized_chunk = chunk.split(' ')
            match_pct = 0.0
            for word in tokenized_chunk:
                for keyword in self.keywords:
                    if fuzz.ratio(word, keyword) > 50:
                        # Increase match % based on keyword strength and frequency
                        match_pct += (1.0 - match_pct) * self.keywords[keyword] * (fuzz.ratio(word, keyword) / 100)
            
            if match_pct > min_thresh:
                start = text.find(chunk)
                end = start + len(chunk)
                context_matches.append(
                    {'start': start, 'end': end, 'data': chunk, 'match_pct': match_pct})
        
        logger.debug(f'{self.__str__()} Contextual Matches: {context_matches}')
        return context_matches
    
    @abc.abstractmethod
    def detect_pii(self, text, tagged_text) -> list:
        raise NotImplementedError
