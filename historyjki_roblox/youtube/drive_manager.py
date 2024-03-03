import os

from historyjki_roblox.youtube.drive_relayer import DriveRelayer
from historyjki_roblox.resource_manager import ResourceManager


class DriveManager:

    def __init__(self):
        self.drive_relayer = DriveRelayer()
        self.resource_manager = ResourceManager()
        self.files = self._get_all_files()
        for k, v in self.files.items():
            name, parent = k
            print(name, v, parent)

    def _get_all_files(self, parent: str = "root"):
        files = {}
        for file in self.drive_relayer._search_file(f"'{parent}' in parents"):
            key = (file["name"], parent)
            files[key] = file["id"]
            if file["mimeType"] == "application/vnd.google-apps.folder":
                files.update(self._get_all_files(file["id"]))
        return files

    def _check_if_file_exists(self, file_path: str, folder_id: str) -> str:
        file_name = os.path.basename(file_path)
        k = (file_name, folder_id)
        if k in self.files:
            return self.files[k]
        return None

    def _upload_folder(self, folder_path: str, parent: str = "root"):
        print(f"uploading {folder_path}, parent: {parent}")
        folder_id = self._check_if_file_exists(folder_path, parent)
        if folder_id is None:
            folder_id = self.drive_relayer._create_file(folder_path, True, parent)

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                if self._check_if_file_exists(item_path, folder_id) is None:
                    self.drive_relayer._create_file(item_path, False, folder_id)
            elif os.path.isdir(item_path):
                self._upload_folder(item_path, folder_id)

    def _update(self):
        self._upload_folder(self.resource_manager._get_absolute_path("output"))
        # self._upload_folder(self.resource_manager._get_absolute_path("output"))


if __name__ == "__main__":
    drive_manager = DriveManager()
    drive_manager._update()
