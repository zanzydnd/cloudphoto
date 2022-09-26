import sys
from pathlib import Path

import boto3

from cloudphoto.delete import FileDeleter
from cloudphoto.download import FileDownloader
from cloudphoto.initializer import init_cloudphoto
from cloudphoto.list import FileLister
from cloudphoto.site import SiteMaker
from cloudphoto.uploading import FileUploader
from cloudphoto.utils import is_configured, read_config


def upload(client, bucket_name):
    params = {"album": None, "path": None}

    try:
        params[sys.argv[2][2:]] = sys.argv[3]
    except Exception as e:
        raise Exception("Не хватает параметров")

    try:
        params[sys.argv[4][2:]] = sys.argv[5]
    except Exception as e:
        pass

    if not params.get("album"):
        raise Exception("Введите параметр album")

    if params.get("album").find("/") != -1:
        raise Exception("Параметр album не может содержать символ /")

    uploader = FileUploader(
        s3_client=client, album_name=params.get("album"), bucket_name=bucket_name
    )
    uploader.upload(Path(params.get("path")))


def download(client, bucket_name):
    params = {"album": None, "path": None}

    try:
        params[sys.argv[2][2:]] = sys.argv[3]
    except Exception as e:
        raise Exception("Не хватает параметров")

    try:
        params[sys.argv[4][2:]] = sys.argv[5]
    except Exception as e:
        pass

    if not params.get("album"):
        raise Exception("Введите параметр album")

    downloader = FileDownloader(
        s3_client=client, album_name=params.get("album"), bucket_name=bucket_name
    )

    if params.get("path"):
        downloader.download(Path(params.get("path")))
    else:
        downloader.download()


def list(client, bucket_name):
    params = {
        "album": None,
    }

    try:
        params[sys.argv[2][2:]] = sys.argv[3]
    except Exception as e:
        pass

    lister = FileLister(
        s3_client=client, album_name=params.get("album"), bucket_name=bucket_name
    )

    lister.list()


def delete(client, bucket_name):
    params = {"album": None, "photo": None}

    try:
        params[sys.argv[2][2:]] = sys.argv[3]
    except Exception as e:
        raise Exception("Не хватает параметров")

    try:
        params[sys.argv[4][2:]] = sys.argv[5]
    except Exception as e:
        pass

    if not params.get("album"):
        raise Exception("Введите параметр album")

    deleter = FileDeleter(
        s3_client=client, album_name=params.get("album"), bucket_name=bucket_name
    )

    if params.get("photo"):
        deleter.delete(params.get("photo"))
    else:
        deleter.delete()


def mksite(client, bucket_name):
    is_configured()
    site_maker = SiteMaker(client, bucket_name)
    site_maker.make_site()


def init(**kwargs):
    init_cloudphoto()


COMMANDS_NAME_AND_FUNCTIONS = {
    "upload": upload,
    "download": download,
    "list": list,
    "delete": delete,
    "init": init,
    "mksite": mksite,
}


def main():
    sys.tracebacklimit = -1
    try:
        command = sys.argv[1]
    except Exception as e:
        raise Exception("Введите команду")

    function = COMMANDS_NAME_AND_FUNCTIONS.get(command)

    if function:
        client = None
        bucket_name = None
        if command != "init":
            is_configured()
            session = boto3.session.Session()
            config = read_config()
            client = session.client(
                service_name="s3",
                endpoint_url=config.get("DEFAULT", "endpoint_url"),
                aws_access_key_id=config.get("DEFAULT", "aws_access_key_id"),
                aws_secret_access_key=config.get("DEFAULT", "aws_secret_access_key"),
                region_name=config.get("DEFAULT", "region"),
            )
            bucket_name = config.get("DEFAULT", "bucket")

        function(client=client, bucket_name=bucket_name)
    else:
        raise Exception(
            f"Неверная команда. Доступные: {COMMANDS_NAME_AND_FUNCTIONS.keys()}"
        )


if __name__ == "__main__":
    main()
