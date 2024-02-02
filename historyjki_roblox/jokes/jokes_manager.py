import argparse
import datetime
import re

from typing import Optional

from historyjki_roblox.resource_manager import ResourceManager
from historyjki_roblox.story.story_parser_gpt import GptStoryParser
from historyjki_roblox.youtube.youtube_manager import YoutubeManager
from historyjki_roblox.video.video_builder import HeadlessVideoBuilder


class JokesManager:

    def __init__(self):
        self.headless_video_builder = HeadlessVideoBuilder()
        self.story_parser = GptStoryParser()
        self.resource_manager = ResourceManager()
        self.youtube_manager = YoutubeManager()

    def merge_jokes_with_youtube(self):
        self.youtube_manager.download_videos_data()
        youtube_data = self.resource_manager.get_youtube_data()
        shorts_videos = [
            i
            for i in youtube_data["videos"]
            if re.match(r"^PT\d{1,2}S$", i["duration"])
        ]
        shorts_title_map = {i["title"]: i for i in shorts_videos}
        shorts_id_map = {i["id"]: i for i in shorts_videos}

        jokes_data = self.resource_manager.get_jokes_data()

        for joke in jokes_data["jokes"]:
            title, video_id = joke["title"], joke["videoId"]
            if title in shorts_title_map:
                joke["videoId"] = shorts_title_map[title]["id"]

            if video_id in shorts_id_map:
                joke["title"] = shorts_id_map[video_id]["title"]

        self.resource_manager.update_jokes_data(jokes_data)
        print("Merge done.")

    def parse_scenarios(self): ...

    def render_videos(self):
        jokes_data = self.resource_manager.get_jokes_data()
        for joke in jokes_data["jokes"]:
            if joke["videoFileName"] is not None:
                continue
            if joke["videoId"] is not None:
                continue

            joke_raw = self.resource_manager.read_joke_parsed(
                joke["jokeCategory"], joke["number"]
            )
            story = self.story_parser.parse_raw_story(joke_raw)
            self.headless_video_builder.build_video(
                story=story, is_video_horizontal=False
            )
            video_path = self.headless_video_builder.save()
            joke["videoFileName"] = video_path.split("/")[-1]

        self.resource_manager.update_jokes_data(jokes_data)

    def upload_jokes(
        self, status: str = "private", number_of_days_ahead: int = 0, hour: int = 0
    ):
        print(f"Upload, status: {status}, day: +{number_of_days_ahead}, hour: {hour}")
        youtube_titles = [
            i["title"] for i in self.resource_manager.get_youtube_data()["videos"]
        ]
        jokes_data = self.resource_manager.get_jokes_data()
        for joke in jokes_data["jokes"]:
            if joke["videoFileName"] is None:
                continue
            if joke["videoId"] is not None:
                continue
            if joke["title"] in youtube_titles:
                continue

            joke_raw = self.resource_manager.read_joke_raw(
                joke["jokeCategory"], joke["number"]
            )
            description = "Coś z humorkiem :)\n\n" + joke_raw

            video_file_path = self.resource_manager.get_video_save_path(
                video_name=joke["videoFileName"]
            )

            publish_at = None
            if number_of_days_ahead is not None and hour is not None:
                publish_at = (
                    datetime.datetime.now()
                    + datetime.timedelta(days=number_of_days_ahead)
                ).replace(hour=hour, minute=0, second=0).isoformat()
            print(publish_at)

            self.youtube_manager.upload_video(
                video_file_path, joke["title"], description, status, publish_at
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jokes manager.")
    parser.add_argument(
        "operation",
        choices=["yt-merge", "render", "upload"],
        help="Operation to perform",
    )
    parser.add_argument(
        "-S", "--status", type=str, default="private", help="Video publication status"
    )
    parser.add_argument("-D", "--days", type=int, help="Number of days ahead")
    parser.add_argument("-H", "--hour", type=int, help="Hour")
    args = parser.parse_args()

    jokes_manager = JokesManager()
    if args.operation == "yt-merge":
        jokes_manager.merge_jokes_with_youtube()
    elif args.operation == "render":
        jokes_manager.render_videos()
    elif args.operation == "upload":
        print(args.status)
        jokes_manager.upload_jokes(
            status=args.status, number_of_days_ahead=args.days, hour=args.hour
        )
