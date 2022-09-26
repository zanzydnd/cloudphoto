from abc import ABC

from botocore.client import BaseClient


class S3StorageWorker(ABC):
    def __init__(self, s3_client: BaseClient, bucket_name: str, album_name: str = None):
        self.client = s3_client
        self.album_name = album_name
        self.bucket_name = bucket_name

    def is_album_exists(self) -> bool:
        for key in self.client.list_objects(
            Bucket=self.bucket_name,
            Prefix=self.album_name + "/",
            Delimiter="/",
        )["Contents"]:
            return True
        return False
