import os
from datetime import datetime

import requests
from flask import request
from flask_restful import Resource
from loguru import logger

from core.aws import download_s3_file
from main import redact_data, text_to_pii


class PredictText(Resource):
    def post(self):
        """
        Detects PII in plain-text and returns the redacted text, along with an array of PII markers and their
        locations.
        :return: Dict:
        redacted: Fully redacted text
        markers: List of PII markers detected along with their locations and confidences
        """
        body = request.get_json(force=True)
        text = body.get('text')
        
        pii = text_to_pii(text)  # Detect PII in the given text stream
        redacted_text = redact_data(text, pii)
        
        logger.debug(pii)
        
        return {'redacted': redacted_text, 'markers': pii}


class PredictFile(Resource):
    def post(self):
        body = request.get_json(force=True)
        job_id = body.get('job_id')
        
        # Base API information, headers and URL
        url_base = f'http://{os.getenv("API_HOST")}:{os.getenv("API_PORT")}'
        headers = {'Authorization': f'Bearer {os.getenv("MODEL_KEY")}'}
        
        # Get the job information, including dataset ID
        job_url = f'{url_base}/job/{job_id}'
        
        job_response = requests.get(url=job_url, headers=headers)
        dataset_id = job_response.json().get('dataset_id')
        
        # Get dataset information and location
        dataset_url = f'{url_base}/dataset/{dataset_id}'
        
        dataset_response = requests.get(url=dataset_url, headers=headers).json()
        
        # Download file from S3 and parse
        output_location = download_s3_file(dataset_response.get('location'))
        
        f = open(output_location, 'r')
        text = f.read()
        pii = text_to_pii(text)
        
        job_passed = True
        
        for marker in pii:
            logger.debug(f'Posting marker: {marker}')
            pii_url = f'{url_base}/pii/text_file'
            payload = {
                'dataset_id': dataset_id,
                'pii_type': marker.get('pii_type'),
                'start_location': marker.get('start_location'),
                'end_location': marker.get('end_location'),
                'confidence': marker.get('confidence')
            }
            logger.debug(f'Payload: {payload}')
            r = requests.post(url=pii_url, headers=headers, json=payload)
            
            if r.status_code != 200:
                logger.error(r.content.decode())
                job_passed = False
        
        job_status_url = f'{url_base}/job/{job_id}'
        if job_passed:  # Perform clean-up
            logger.debug('Job passed...')
            payload = {'job_status': 'COMPLETE', 'job_completed_ts': str(datetime.now())}
            r = requests.patch(url=job_status_url, headers=headers, json=payload)
        else:
            logger.debug('Job failed...')
            payload = {'job_status': 'FAILED', 'job_completed_ts': str(datetime.now())}
            r = requests.patch(url=job_status_url, headers=headers, json=payload)
        
        os.remove(output_location)
        
        return pii
