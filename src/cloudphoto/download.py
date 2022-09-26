from pathlib import Path

from cloudphoto.base import S3StorageWorker


class FileDownloader(S3StorageWorker):
    def download(self, path: Path = Path.cwd()):
        if not self.is_album_exists():
            raise Exception("Не существует такого альбома.")

        if not path.is_dir():
            raise Exception("Путь не является директорией.")

        for key in self.client.list_objects(
            Bucket=self.bucket_name, Prefix=self.album_name + "/", Delimiter="/"
        )["Contents"]:
            get_object_response = self.client.get_object(
                Bucket=self.bucket_name, Key=key["Key"]
            )
            filename = key["Key"].split("/")[1]

            filepath = path / filename
            with filepath.open("w") as f:
                f.write(get_object_response["Body"].read())
