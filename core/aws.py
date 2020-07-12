import os
from urllib.parse import urlparse

import boto3
from loguru import logger


def download_s3_file(file_location, tmp_dir='../tmp_files') -> str:
    """
    Downloads a file from AWS S3 at a given location using the SpotlightAI credentials. Stores the downloaded
    file in a temporary local location.
    :param file_location: String file location / S3 path
    :param tmp_dir: Directory name to temporarily store file.
    :return: Temporary filepath location of the downloaded file.
    """
    logger.info(f'Downloading file {file_location} from AWS...')
    s3_client = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                             aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    
    parsed_path = urlparse(file_location)
    
    bucket_name = parsed_path.netloc.split('.')[0] if parsed_path.scheme == 's3' else parsed_path.netloc.split('.')[0]
    object_name = parsed_path.path.lstrip('/')
    
    logger.debug(f'Bucket Name: {bucket_name}, Object Name: {object_name}')
    
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    
    output_location = f'{tmp_dir}/{object_name.replace("/", "__")}'
    s3_client.download_file(bucket_name, object_name, output_location)
    
    logger.debug(f'File successfully downloaded to {output_location}')
    
    return output_location
