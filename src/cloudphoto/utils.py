import configparser
import os
import pathlib

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def read_config() -> configparser.ConfigParser:
    home = pathlib.Path.home()
    config_path = home / ".config" / "cloudphoto" / "cloudphotorc"
    config = configparser.ConfigParser()
    config.read(str(config_path))

    return config


def is_configured():
    home = pathlib.Path.home()
    config_path = home / ".config" / "cloudphoto" / "cloudphotorc"
    config = configparser.ConfigParser()
    config.read(str(config_path))

    if not config["DEFAULT"]:
        raise Exception("Запустите init")
