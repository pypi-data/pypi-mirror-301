import os
from io import BytesIO
from typing import BinaryIO

import boto3  # type: ignore

from .protocol import DatalakeProtocol


class S3Client:
    def __init__(self, aws_client) -> None:
        self.client = aws_client

    @staticmethod
    def build() -> "DatalakeProtocol":
        AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
        AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
        return S3Client(
            boto3.client(
                "s3",
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY,
            )
        )

    def download_object(self, bucket_name: str, obj_name, dest_file_path):
        self.client.download_file(bucket_name, obj_name, dest_file_path)

    def download_object_as_file(self, bucket_name: str, obj_name: str, f: BinaryIO):
        data = BytesIO()
        self.client.download_fileobj(bucket_name, obj_name, data)
        data.seek(0)
        return data
