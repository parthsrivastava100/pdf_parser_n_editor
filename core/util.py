import os
import pickle

import nltk
from loguru import logger
from nltk.corpus import conll2000

from chunkers import BigramChunker
from constants.base import PII_CATEGORIES, PII_DESCRIPTIONS


def preprocess_text(text) -> list:
    """
    Transforms a plaintext string into a tokenized 2-D array with part-of-speech, named entity and IOB tags.
    :param text: Plaintext string
    :return: 2-D tokenized array of processed text
    """
    logger.info('Starting text preprocessing...')
    
    # Tokenize text into words and sentences
    tokenized_sentences = [nltk.word_tokenize(s) for s in nltk.sent_tokenize(text)]
    logger.debug(f'Tokenized Sentences: {tokenized_sentences}')
    
    # Apply part-of-speech tags to each token
    pos_tagged = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    logger.debug(f'POS Tags: {pos_tagged}')
    
    # Apply named entity and IOB tags to each token
    chunker = train_chunker()
    
    final_output = []
    
    for sentence in pos_tagged:
        sentence_output = []
        ne_result = nltk.tree2conlltags(nltk.ne_chunk(sentence))
        iob_result = nltk.tree2conlltags(chunker.parse(sentence))
        
        for i, token in enumerate(ne_result):  # Combine named entity result and IOB result
            output = token + (iob_result[i][2],)
            sentence_output.append(output)
        
        final_output.append(sentence_output)
    
    logger.debug(f'Fully Tagged: {final_output}')
    return final_output


def train_chunker(save_filepath='./models/chunker.pkl', force_train=False):
    """
    Returns a BigramChunker model for the IOB tagging model. This model can be trained fresh or loaded from a file.
    :param save_filepath: Filepath to store the saved model or load a previously saved model.
    :param force_train: Force a new training of the chunker model
    :return: BigramChunker model instance
    """
    if not os.path.exists(save_filepath) or force_train:
        logger.info('Training new chunker model...')
        train_sents = conll2000.chunked_sents('train.txt')
        chunker = BigramChunker(train_sents)
        
        with open(save_filepath, 'wb') as f:
            pickle.dump(chunker, f)
    else:
        logger.info(f'Reading chunker model from file: {save_filepath}')
        with open(save_filepath, 'rb') as f:
            chunker = pickle.load(f)
    
    return chunker


def format_pii_object(start, end, pii_type, confidence) -> object:
    return {
        "start_location": start,
        "end_location": end,
        "pii_type": pii_type,
        "confidence": confidence,
        "long_description": PII_DESCRIPTIONS.get(pii_type, ''),
        "category": PII_CATEGORIES.get(pii_type, '')
    }


def capitalize_first_letters(text):
    return ' '.join([word.capitalize() for word in text.split(' ')])
