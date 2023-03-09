import os
import boto3
# from dotenv import load_dotenv
from botocore.exceptions import ClientError
from pathlib import Path
from DB import logger
from db_credentials import s3_access_key, s3_secret_key

REGION = dict(US="US", DE="DE")  # key => value := region_value_in_mongo => region_value_in_cos_environment


class S3Handler:
    """
    Manage call to S3 APIs
    """

    def __init__(self, **kwargs):
        self.setup()
        self.location = REGION.get(kwargs.get('location'), REGION['US'])
        self.s3 = self.connect()

    def setup(self) -> None:
        # initial setup of project
        try:
            # For local setup load S3 environment variables from .s3credentials file,
            s3_env_path = Path(__file__).parents[0].absolute().joinpath(
                '.s3credentials'
            )
            if os.path.exists(s3_env_path):
                load_dotenv(dotenv_path=s3_env_path)

        except Exception as e:
            logger.error(e)

    def connect(self):
        """
        Establish connection to S3
        ACCESS KEY
        SECRET KEY
        ENDPOINT
        :return: An instance of boto3
        """
        s3 = None
        try:

            logger.info('connect::START')
            s3 = boto3.client(
                's3',
                aws_access_key_id=os.getenv(s3_access_key).strip(),
                aws_secret_access_key=os.getenv(s3_secret_key).strip(),
                endpoint_url=os.getenv("S3_HOST").strip()
            )
            logger.info(f'connection successfully established for {self.location}')
            return s3
        except Exception as e:
            logger.error(e)
        finally:
            logger.info('connect::END')

    def download_imported_file(self, audit_id: str, scriptPath: str, bucket: str = ''):
        if not bucket:
            bucket: str = os.getenv("S3_CNA_BUCKET").strip()
        try:
            logger.info('Bucket is: {}'.format(bucket))
            file_name = audit_id + '.zip'
            s3_path = scriptPath + '//' + file_name
            logger.info('imported_file_download::START')
            self.s3.download_file(bucket, file_name, s3_path)
        except Exception as e:
            logger.error(e)
        finally:
            logger.info('get_imported_file::END')
