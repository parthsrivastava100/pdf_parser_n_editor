import csv
import re
import pdf_redactor
import nltk
from dotenv import find_dotenv, load_dotenv
from loguru import logger

from core import util
from parsers.markers.cc_number import CCNumberParser
from parsers.markers.ein import EINParser
from parsers.markers.email import EmailParser
from parsers.markers.finance.routing import RoutingNumberParser
from parsers.markers.gender import GenderParser
from parsers.markers.location.city import CityParser
from parsers.markers.location.country import CountryParser
from parsers.markers.name import NameParser
from parsers.markers.phone import USAPhoneParser
from parsers.markers.ssn import SSNParser
from parsers.markers.ip_address import IPAddressParser
from parsers.markers.company import CompanyParser

# Download and install necessary NLTK packages.
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('conll2000', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)

# load_dotenv(find_dotenv())

logger.add("model_run.log", enqueue=True)


def redact_data(text, pii_markers):
    output_text = ""
    
    current_pos = 0
    sorted_markers = sorted(pii_markers, key=lambda k: k['start_location'])
    
    for marker in sorted_markers:
        output_text += text[current_pos:marker.get('start_location')]
        output_text += "****"
        current_pos = marker.get('end_location')
    
    output_text += text[current_pos:]
    
    return output_text


def text_to_pii(text):
    """
    Detects multiple PII markers in a blob of plaintext.
    :param text: String of plaintext.
    :return: Dictionary of PII markers detected.
    """
    tagged_text = util.preprocess_text(text)
    
    parsers = [SSNParser(), EmailParser(), USAPhoneParser(), GenderParser(), EINParser(), CCNumberParser(),CompanyParser(),
               CityParser(), CountryParser(), NameParser(), IPAddressParser(), RoutingNumberParser()]
    
    pii = []
    for parser in parsers:
        pii.extend(parser.detect_pii(text, tagged_text))
    
    return pii


def csv_to_pii(file):
    pii = []
    
    columns = {}
    indices = {}
    with open(file) as f:
        reader = csv.reader(f)
        for i, lines in enumerate(reader):
            for j, value in enumerate(lines):
                if i == 0:
                    columns[value] = ""
                    indices[j] = value
                else:
                    columns[indices[j]] += f" {lines[j]}"
    
    for i, column in enumerate(columns):
        pii_detected = text_to_pii(columns[column].strip())
        
        types_detected = set()
        for detected in pii_detected:
            types_detected.add(detected.get('type'))
        
        if len(types_detected) != 0:
            pii.append({'column': i, 'pii_detected': list(types_detected)})
    
    return pii


if __name__ == "__main__":
    DIRECTORY = './sample_data/'
    
    input_file = 'cc.pdf'
    
    text_file = f'{DIRECTORY}{input_file}'
    if(input_file.endswith('.pdf')):
        options = pdf_redactor.RedactorOptions()
        options.xmp_filters = [lambda xml : None]
        options.content_filters = [
	    (
		re.compile(r"comment!"),
		lambda m : "annotation?"
	    ),
        ]
        pdf_redactor.redactor(options,text_file)
    else:

    
        logger.info(f'Scanning PII in {input_file}')
    
        text = open(text_file, 'r').read()
    
        logger.debug(f'Scanning text: {text}')
    
        pii = text_to_pii(text)
    
        logger.debug(f'PII Detected: {pii}')
    
        for item in pii:
            pii_type = item.get('pii_type')
        
            logger.info(f'{item.get("pii_type")}: {text[item.get("start_location"):item.get("end_location")]} '
                    f'({round(item.get("confidence"), 2) * 100}%)')
