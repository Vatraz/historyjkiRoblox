from typing import List, Optional

from historyjki_roblox.resource_manager import ResourceManager
from historyjki_roblox.youtube.youtube_relayer import YoutubeRelayer


class YoutubeManager:

    def __init__(self):
        self.resource_manager = ResourceManager()
        self.youtube_relayer = YoutubeRelayer()
        self.videos_data = self._read_data()

    def _read_data(self):
        return self.resource_manager.read_youtube_data()

    def _save(self):
        self.resource_manager.update_videos_data(self.videos_data)

    def _get_video_data(self, video_id: str):
        if video_id in self.videos_data:
            return self.videos_data[video_id]
        return None

    def _download_videos_data(self):
        video_ids = self.youtube_relayer.get_my_videos()
        videos_data = self.youtube_relayer.get_videos_data(video_ids)
        self.videos_data = videos_data
        self._save()

    def _upload_video(
        self,
        video_file_path: str,
        title: str,
        description: str,
        tags: List[str],
        status: str,
        publish_at: Optional[str] = None,
    ):
        video_id, video_data = self.youtube_relayer.upload_video(
            video_file_path, title, description, tags, status, publish_at
        )

        self.videos_data[video_id] = video_data
        self._save()
        return video_id, video_data
