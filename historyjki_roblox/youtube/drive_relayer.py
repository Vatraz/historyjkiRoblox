import os
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.appdata",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.metadata",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.photos.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


class DriveRelayer:

    def __init__(self):
        self.service = self._build_service()

    def _build_service(self):
        creds = None
        token_pickle_file = "drive_token.pickle"

        if os.path.exists(token_pickle_file):
            with open(token_pickle_file, "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secret.json", SCOPES
                )
                creds = flow.run_local_server()

            with open(token_pickle_file, "wb") as token:
                pickle.dump(creds, token)

        return build("drive", "v3", credentials=creds)

    def _create_folder(self, folder_name: str, parent: str | None = None) -> str:
        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
        }

        if parent is not None:
            file_metadata["parents"] = [parent]

        folder = self.service.files().create(body=file_metadata, fields="id").execute()
        return folder.get("id")

    def _create_file(
        self, file_path: str, is_folder: bool, parent: str | None = None
    ) -> str:
        file_metadata, media = {"name": os.path.basename(file_path)}, None

        if is_folder is True:
            file_metadata["mimeType"] = "application/vnd.google-apps.folder"
        else:
            media = MediaFileUpload(file_path)

        if parent is not None:
            file_metadata["parents"] = [parent]

        file = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        return file.get("id")

    def _search_file(self, q: str | None = None):
        files, page_token = [], None
        response = (
            self.service.files()
            .list(
                q=q,
                fields="nextPageToken, files(id, name, mimeType)",
                pageToken=page_token,
                pageSize=50,
            )
            .execute()
        )

        for file in response.get("files", []):
            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break

        return files
