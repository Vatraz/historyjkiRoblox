from typing import Optional

from historyjki_roblox.resource_manager import ResourceManager
from historyjki_roblox.youtube.youtube_relayer import YoutubeRelayer


class YoutubeManager:

    def __init__(self):
        self.resource_manager = ResourceManager()
        self.youtube_relayer = YoutubeRelayer()

    def upload_video(
        self,
        video_file_path: str,
        title: str,
        description: str,
        status: str,
        publish_at: Optional[int] = None,
    ):
        result = self.youtube_relayer.upload_video(
            video_file_path, title, description, status, publish_at
        )

    def download_videos_data(self):
        videos = self.youtube_relayer.get_my_videos()
        videos_data = self.youtube_relayer.get_videos_data(videos)
        self.resource_manager.update_videos_data(videos_data)


if __name__ == "__main__":
    manager = YoutubeManager()
    manager.download_videos_data()
