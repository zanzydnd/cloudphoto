import pathlib
from pathlib import Path

import boto3

from cloudphoto.delete import FileDeleter
from cloudphoto.download import FileDownloader
from cloudphoto.list import FileLister
from cloudphoto.uploading import FileUploader

session = boto3.session.Session()

s3 = session.client(
    service_name="s3",
    endpoint_url="https://storage.yandexcloud.net",
    # aws_access_key_id=
    # aws_secret_access_key=
)

# uploader = FileUploader(s3, album_name="first_album")

# Если каталог с именем PHOTOS_DIR не доступен, то программа cloudphoto должна завершиться с ошибкой.
# dir_path = Path(".")
# if not dir_path.is_dir():
#     raise Exception(
#         f"{dir_path.name} не является директорией"
#     )
# uploader.upload(dir_path)

# downloader = FileDownloader(s3, album_name="asd")
# downloader.download()

# lister = FileLister(s3)
# lister.list()

deleter = FileDeleter(s3, album_name="asd")
deleter.delete("asd")

import configparser

config = configparser.ConfigParser()
home = pathlib.Path.home()
config_path = home / ".config" / "cloudphoto" / "cloudphotorc"
config.read(config_path)

config.get("")
