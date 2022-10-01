import os

from jinja2 import Environment, FileSystemLoader, Template

from cloudphoto.base import S3StorageWorker
from cloudphoto.template import album_page, index, error
from cloudphoto.utils import ROOT_DIR


class SiteMaker(S3StorageWorker):
    def __init__(self, client, bucket_name):
        super().__init__(client, bucket_name)
        self.url = f"https://{bucket_name}.website.yandexcloud.net/"

    def make_site(self):
        # file_loader = FileSystemLoader("templates")
        # env = Environment(loader=file_loader)

        albums = {}

        for key in self.client.list_objects(Bucket=self.bucket_name)["Contents"]:
            try:
                album_name, img_name = key["Key"].split("/")
                if not albums.get(album_name):
                    albums[album_name] = [img_name]
                else:
                    albums[album_name].append(img_name)

            except Exception:
                pass

        albums_indexed = []
        i = 0
        for album_name in albums.keys():
            rendered_album = Template(album_page).render(
                album=album_name, images=albums.get(album_name), url=self.url
            )
            i += 1
            with open(ROOT_DIR + "/tmp.html", "w") as f:
                f.write(rendered_album)
            self.client.upload_file(
                ROOT_DIR + "/tmp.html",
                self.bucket_name,
                f"album{i}.html",
            )
            os.remove(ROOT_DIR + "/tmp.html")
            albums_indexed.append(
                {
                    "album_numbered_name": f"album{i}",
                    "album_name": album_name,
                }
            )
        rendered_index = Template(index).render(albums=albums_indexed)
        with open(ROOT_DIR + "/tmp.html", "w") as f:
            f.write(rendered_index)
        self.client.upload_file(
            ROOT_DIR + "/tmp.html",
            self.bucket_name,
            f"index.html",
        )
        with open(ROOT_DIR + "/tmp.html", "w") as f:
            f.write(error)
        self.client.upload_file(
            ROOT_DIR + "/tmp.html",
            self.bucket_name,
            f"error.html",
        )
        os.remove(ROOT_DIR + "/tmp.html")

        website_configuration = {
            "ErrorDocument": {"Key": "error.html"},
            "IndexDocument": {"Suffix": "index.html"},
        }

        self.client.put_bucket_website(
            Bucket=self.bucket_name, WebsiteConfiguration=website_configuration
        )

        print(self.url)
