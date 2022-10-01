from botocore.exceptions import ClientError

from cloudphoto.base import S3StorageWorker


class FileDeleter(S3StorageWorker):
    def _delete_full_album(self):
        for_deletion = [
            {"Key": key.get('Key')}
            for key in self.client.list_objects(
                Bucket=self.bucket_name,
                Prefix=self.album_name + "/",
                Delimiter="/",
            )["Contents"]
        ]

        self.client.delete_objects(
            Bucket=self.bucket_name, Delete={"Objects": for_deletion}
        )

    def _delete_photo(self, photo_name: str):
        full_obj_path = self.album_name + "/" + photo_name
        try:
            self.client.get_object(
                Bucket=self.bucket_name, Key=full_obj_path
            )
        except ClientError as err:
            if err.response["Error"]["Code"] == "NoSuchKey":
                raise Exception("Нет такого файла")
        for_deletion = [{"Key": full_obj_path}]
        self.client.delete_objects(
            Bucket=self.bucket_name, Delete={"Objects": for_deletion}
        )

    def delete(self, photo_name: str = ""):
        if not self.is_album_exists():
            raise Exception("Не существует такого альбома.")

        if photo_name:
            self._delete_photo(photo_name)
        else:
            self._delete_full_album()
