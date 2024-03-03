import os
import pickle

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from typing import Dict, List

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


class YoutubeRelayer:

    def __init__(self):
        self.scopes = [
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/youtube.upload",
        ]
        self.service = self._build_service()

    def _build_service(self):
        creds = None
        token_pickle_file = "token.pickle"

        if os.path.exists(token_pickle_file):
            with open(token_pickle_file, "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secret.json", self.scopes
                )
                creds = flow.run_local_server()

            with open(token_pickle_file, "wb") as token:
                pickle.dump(creds, token)

        return build("youtube", "v3", credentials=creds)

    def get_my_videos(self) -> List[str]:
        # Returns video ids of account
        page_token, videos = None, []
        while True:
            request = self.service.search().list(
                part="id",
                type="video",
                forMine=True,
                maxResults=50,
                pageToken=page_token,
            )
            response = request.execute()

            for item in response["items"]:
                videos.append(item["id"]["videoId"])

            if "nextPageToken" not in response:
                break

            page_token = response["nextPageToken"]

        return videos

    def get_videos_data(self, videos: List[str]):
        data, page_token, max_result = {}, None, 50
        for i in range(0, len(videos), 50):
            ids = ",".join(videos[i : i + max_result])
            request = self.service.videos().list(
                id=ids,
                part="snippet,contentDetails,status",
                maxResults=50,
                pageToken=page_token,
            )
            response = request.execute()

            if "nextPageToken" in response:
                page_token = response["nextPageToken"]

            for item in response["items"]:
                print(item["snippet"])
                video_id = item["id"]
                data[video_id] = {
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "tags": (
                        item["snippet"]["tags"] if "tags" in item["snippet"] else None
                    ),
                    "duration": item["contentDetails"]["duration"],
                    "status": item["status"]["privacyStatus"],
                    "publishedAt": item["snippet"]["publishedAt"],
                }
        return data

    def upload_video(
        self,
        video_file_path: str,
        title: str,
        description: str,
        tags: List[str] = None,
        privacy_status: str = "private",
        publish_at: str | None = None,
    ) -> Dict:
        request_body = {
            "snippet": {"title": title, "description": description, "tags": tags},
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False,
            },
        }

        if publish_at is not None:
            request_body["status"]["publishAt"] = publish_at

        media = MediaFileUpload(video_file_path)

        response = (
            self.service.videos()
            .insert(
                part="snippet,contentDetails,status",
                body=request_body,
                media_body=media,
            )
            .execute()
        )

        video_data = {
            "title": response["snippet"]["title"],
            "description": response["snippet"]["description"],
            "tags": (
                response["snippet"]["tags"] if "tags" in response["snippet"] else None
            ),
            "duration": response["contentDetails"]["duration"],
            "status": response["status"]["privacyStatus"],
            "publishedAt": response["snippet"]["publishedAt"],
        }

        return response["id"], video_data


if __name__ == "__main__":
    yt = YoutubeRelayer()
    videos = yt.get_my_videos()
    print(len(videos))
