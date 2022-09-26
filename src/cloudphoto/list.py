from cloudphoto.base import S3StorageWorker


class FileLister(S3StorageWorker):
    def _list_albums(self):
        name_set = set()
        for key in self.client.list_objects(Bucket=self.bucket_name)["Contents"]:
            name_set.add(key["Key"].split("/")[0])

        if len(name_set) == 0:
            raise Exception("Нет альбомов")

        for name in name_set:
            print(f"- {name}")

    def _list_photos(self):
        photos = []
        for key in self.client.list_objects(
            Bucket=self.bucket_name,
            Prefix=self.album_name + "/",
            Delimiter="/",
        )["Contents"]:
            photos.append(key["Key"].split("/")[1])

        if len(photos) == 0:
            raise Exception("Нет картинок.")

        for photo_name in photos:
            print(f"- {photo_name}")

    def list(self):
        if self.album_name:
            self._list_photos()
        else:
            self._list_albums()
