import logging
from pathlib import Path

from botocore.exceptions import ClientError

from cloudphoto.base import S3StorageWorker


class FileUploader(S3StorageWorker):
    PICTURES_EXTENSIONS = [".jpg", ".jpeg"]

    def _make_object_key_name(self, file_name: str):
        return f"{self.album_name}/{file_name}"

    def upload(self, path: Path):
        """
        Загружает все файлы из директории в облачное хранилище
        :param path: принимает объект Path - путь к директории
        :return:
        """
        photos_count = 0
        for child in path.iterdir():
            if child.is_file() and child.suffix in self.PICTURES_EXTENSIONS:
                try:
                    print(self.bucket_name)
                    self.client.upload_file(
                        str(child),
                        self.bucket_name,
                        self._make_object_key_name(child.name),
                    )
                    photos_count += 1
                except ClientError as e:
                    logging.warning(e)

        if photos_count == 0:
            raise Exception(
                f"В указаной директории нет файлов удволетворяющих расширениям: {self.PICTURES_EXTENSIONS}"
            )
