import os

from typing import List, Optional

from historyjki_roblox.resource_manager import ResourceManager
from historyjki_roblox.story.story_parser_gpt import GptStoryParser
from historyjki_roblox.youtube.youtube_manager import YoutubeManager


class JokesManager:

    def __init__(self):
        self.youtube_manager = YoutubeManager()
        self.resource_manager = ResourceManager()
        self.data = self._load_jokes_data()

    def _load_jokes_data(self) -> dict:
        return self.resource_manager.load_jokes_data()

    def _get_joke_id(self, category: str, filename: str) -> str:
        return category + "__" + os.path.splitext(filename)[0]

    def _get_category_filename_from_id(self, joke_id: str):
        category, filename = joke_id.split("__")
        return category, f"{filename}.txt"

    def _get_data(self):
        self.data = self._load_jokes_data()
        return self.data

    def _get_joke_data(self, joke_id: str):
        video_id = self.data[joke_id]["videoId"]
        return {
            "title": self.data[joke_id]["title"],
            "videoId": video_id,
            "raw": self._get_joke_raw(joke_id),
            "parsed": self._get_joke_parsed(joke_id),
            "isVideoRendered": (
                True if os.path.exists(self._get_vidoe_path(joke_id)) else False
            ),
            "youtube": self.youtube_manager._get_video_data(video_id)
        }

    def _get_joke_raw(self, joke_id: str):
        category, filename = self._get_category_filename_from_id(joke_id)
        return self.resource_manager.get_joke_raw(category, filename)

    def _get_joke_parsed(self, joke_id: str):
        category, filename = self._get_category_filename_from_id(joke_id)
        return self.resource_manager.get_joke_parsed(category, filename)

    def _save_joke_parsed(): ...

    def _add_joke(self, category: str, filename: str, title: str, parsed: str):
        joke_id = self._get_joke_id(category, filename)
        self.resource_manager.save_joke_parsed(category, filename, parsed)
        self.data[joke_id] = {"title": title, "videoId": None}
        self._save()

    def _delete_joke(self, joke_id):
        self.data.pop(joke_id)
        parsed_path = self._get_parsed_path(joke_id)
        if os.path.exists(parsed_path):
            os.remove(parsed_path)
        video_path = self._get_vidoe_path(joke_id)
        if os.path.exists(video_path):
            os.remove(video_path)
        self._save()

    def _delete_joke_video(self, joke_id):
        os.remove(self._get_vidoe_path(joke_id))

    def _get_categories(self):
        return self.resource_manager.get_jokes_categories()

    def _get_available_jokes_for_category(self, category):
        existing_jokes = [
            f"{i.split('__')[1]}.txt"
            for i in self.data.keys()
            if i.startswith(category)
        ]
        available_jokes = [
            i
            for i in self.resource_manager.get_category_jokes(category)
            if i not in existing_jokes
        ]
        return sorted(available_jokes, key=lambda i: int(os.path.splitext(i)[0]))

    def _parse_joke(self, category: str, filename: str):
        # TODO: add parsing witch chatgpt
        joke_raw = self.resource_manager.get_joke_raw(category, filename)
        self.resource_manager.save_joke_parsed(category, filename, joke_raw)
        return joke_raw

    def _get_story(self, joke_id):
        category, filename = self._get_category_filename_from_id(joke_id)
        parsed_joke = self.resource_manager.get_joke_parsed(category, filename)
        return GptStoryParser().parse_raw_story(parsed_joke)

    def _get_parsed_path(self, joke_id):
        category, filename = self._get_category_filename_from_id(joke_id)
        return (
            self.resource_manager.root_path
            + "/data/jokes/parsed/"
            + category
            + "/"
            + filename
        )

    def _get_vidoe_path(self, joke_id: str):
        return self.resource_manager.root_path + "/output/video/" + joke_id + ".mp4"

    def _save(self):
        self.resource_manager.save_jokes_data(self.data)

    def _upload_joke(self, joke_id: str, status: str, publish_at: str | None):
        joke = self.data[joke_id]
        joke_raw = self._get_joke_raw(joke_id)
        description = "Coś z humorkiem :)\n\n" + joke_raw
        tags = [tag.replace("-", " ") for tag in joke_id.split("__")]

        video_path = self._get_vidoe_path(joke_id)
        if os.path.exists(video_path) is False:
            return None

        video_id, video_data = self.youtube_manager._upload_video(
            video_path, joke["title"], description, tags, status, publish_at
        )
        self.data[joke_id]["videoId"] = video_id
        self._save()
        return video_id, video_data
