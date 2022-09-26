import configparser
import pathlib

import boto3
from botocore.exceptions import ClientError


def init_cloudphoto():
    aws_access_key_id = input("aws_access_key_id: ")
    aws_secret_access_key = input("aws_secret_access_key: ")
    bucket = input("bucket: ")
    try:
        session = boto3.session.Session()
        s3 = session.client(
            service_name="s3",
            endpoint_url="https://storage.yandexcloud.net",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        s3.create_bucket(Bucket=bucket)
    except ClientError as e:
        if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            pass
        print(e)

    home = pathlib.Path.home()
    config_path = home / ".config" / "cloudphoto"
    config_path.mkdir(parents=True, exist_ok=True)
    config_path /= "cloudphotorc"

    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        "bucket": bucket,
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        "region": "ru-central-1",
        "endpoint_url": "https://storage.yandexcloud.net"
    }
    # with open(config_path, "w") as f:
    #     f.write(
    #         f"""[DEFAULT]\nbucket = {bucket}\naws_access_key_id = {aws_access_key_id}\naws_secret_access_key = {aws_secret_access_key}\nregion = ru-central1\nendpoint_url = https://storage.yandexcloud.net"""
    #     )
    with open(config_path, "w") as configfile:
        config.write(configfile)
