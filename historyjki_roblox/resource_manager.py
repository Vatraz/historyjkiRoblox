import json
import os
import random
import shutil
import string
from enum import Enum

from PIL import Image, ImageFont


class EmojiCategory(Enum):
    WOW = "w"


class ResourceReadFailed(Exception):
    pass


class ResourceManager:
    def __init__(self):
        self.root_path = os.path.dirname(os.path.dirname(__file__))

    # CHARACTER

    def get_list_of_characters(self):
        return self._listdir(f"{self.root_path}/data/characters")

    def get_random_roblox_character_name(self, requested_gender: str) -> str:
        chosen_gender = "f" if requested_gender == "FEMALE" else "m"
        return random.choice(
            [char for char in self.get_list_of_characters() if chosen_gender in char]
        )

    def get_roblox_character_path(self, character_name: str) -> str:
        return f"{self.root_path}/data/characters/{character_name}"

    # OSKAREK
    def get_list_of_predefined_oskareks(self):
        return self._listdir(f"{self.root_path}/data/oskareks/images")

    def get_list_of_oskareks(self):
        return self._listdir(f"{self.root_path}/output/oskareks")

    def save_oskarek_image(self, image: Image, image_name: str):
        return image.save(f"{self.root_path}/output/oskareks/{image_name}")

    def get_random_oskarek_image_name(self, requested_gender: str) -> str:
        chosen_gender = "f" if requested_gender == "FEMALE" else "m"
        return random.choice(
            [char for char in self.get_list_of_oskareks() if chosen_gender == char[0]]
        )

    def get_random_predefined_oskarek_image_name(self, requested_gender: str) -> str:
        chosen_gender = "f" if requested_gender == "FEMALE" else "m"
        return random.choice(
            [
                char
                for char in self.get_list_of_predefined_oskareks()
                if chosen_gender == char[0]
            ]
        )

    def get_oskarek_path(self, oskarek_name: str) -> str:
        if oskarek_name in self.get_list_of_predefined_oskareks():
            return f"{self.root_path}/data/oskareks/images/{oskarek_name}"
        else:
            return f"{self.root_path}/output/oskareks/{oskarek_name}"

    def get_face_image_path(self, image_name: str) -> str:
        return f"{self.root_path}/data/images/{image_name}"

    def get_roblox_image_path(self, image_name: str) -> str:
        return f"{self.root_path}/data/characters/{image_name}"

    # THUMBNAIL

    def get_list_of_backgrounds(self):
        return self._listdir(f"{self.root_path}/data/thumbnail/background")

    def get_list_of_emoji(self):
        return self._listdir(f"{self.root_path}/data/thumbnail/emoji")

    def get_thumbnail_data(self):
        with open(f"{self.root_path}/data/thumbnail/thumbnail_data.json") as fp:
            data = json.load(fp)
        return data

    def get_thumbnail_background(self):
        return Image.open(
            f"{self.root_path}/data/thumbnail/background/{random.choice(self.get_list_of_backgrounds())}"
        )

    # possible categories: WOW, LAUGH, SAD etc...
    def get_thumbnail_emoji(self, category: EmojiCategory):
        chosen_category = category.value
        chosen_emoji = random.choice(
            [char for char in self.get_list_of_emoji() if chosen_category in char]
        )
        return Image.open(f"{self.root_path}/data/thumbnail/emoji/{chosen_emoji}")

    # HISTORYJKAS
    def get_saved_historyjkas(self):
        return self._listdir(f"{self.root_path}/stories")

    def load_historyjka_data(
        self, filename: str, raise_on_missing: bool = False
    ) -> dict | None:
        try:
            with open(f"{self.root_path}/stories/{filename}") as fp:
                return json.load(fp)
        except Exception as exe:
            if raise_on_missing:
                raise ResourceReadFailed(exe)
            else:
                return None

    def save_historyjka_data(self, filename: str, data: dict):
        with open(f"{self.root_path}/stories/{filename}", "w") as fp:
            json.dump(data, fp)

    def remove_historyjka(self, filename: str):
        os.remove(f"{self.root_path}/stories/{filename}")

    def copy_historyjka(self, original_filename, copy_filename):
        shutil.copy(
            f"{self.root_path}/stories/{original_filename}",
            f"{self.root_path}/stories/{copy_filename}",
        )

    # OTHER
    def get_prompts_data(self):
        with open(f"{self.root_path}/data/stories/prompts.json") as fp:
            prompts = json.load(fp)
        return prompts

    def get_phrase_font(self):
        return ImageFont.truetype(f"{self.root_path}/data/fonts/phrase.otf", size=65)

    def get_voices(self) -> list:
        with open(f"{self.root_path}/data/voices/voices.json", "r") as f:
            voices = json.load(f)
        return voices["voices"]

    def get_gtts_api_key(self) -> str:
        return os.environ.get("GTTS_API_KEY")

    def get_youtube_api_key(self) -> str:
        return os.environ.get("YOUTUBE_API_KEY")

    def get_random_string(self, length: int = 10) -> str:
        characters = string.ascii_letters + string.digits
        return "".join([random.choice(characters) for _ in range(length)])

    def get_dialogue_path(self, dirname: str, text: str) -> str:
        filepath = f"{self.root_path}/output/dialogues/{dirname}"
        if os.path.exists(filepath) is False:
            os.mkdir(filepath)
        filename = text.lower().replace(" ", "_") + ".mp3"
        filepath = filepath + "/" + filename
        return filepath

    def get_video_save_path(self, video_name: str | None = None) -> str:
        if os.path.exists(f"{self.root_path}/output/video") is False:
            os.mkdir(f"{self.root_path}/output/video")
        if video_name:
            video_name = (
                video_name if video_name.endswith(".mp4") else video_name + ".mp4"
            )
        else:
            video_name = self.get_random_string() + ".mp4"
        return f"{self.root_path}/output/video/{video_name}"

    def get_discord_join_path(self) -> str:
        return f"{self.root_path}/data/sounds/discord_join.mp3"

    def get_discord_leave_path(self) -> str:
        return f"{self.root_path}/data/sounds/discord_leave.mp3"

    def get_background_videos(self, is_horizontal: bool = True) -> list[str]:
        last_dir = "horizontal" if is_horizontal is True else "vertical"
        videos_dir = f"{self.root_path}/data/videos/{last_dir}"
        return [f"{videos_dir}/{i}" for i in self._listdir(videos_dir)]

    def get_background_sounds(self) -> list[str]:
        sounds_dir = f"{self.root_path}/data/sounds/background"
        return [f"{sounds_dir}/{i}" for i in self._listdir(sounds_dir)]

    # JOKES
    def read_joke_raw(self, category: str, number: int) -> str:
        return "".join(
            open(
                f"{self.root_path}/data/jokes/raw/{category}/{number}.txt", "r"
            ).readlines()
        )

    def read_joke_parsed(self, category: str, number: int) -> str:
        return "".join(
            open(
                f"{self.root_path}/data/jokes/parsed/{category}/{number}.txt", "r"
            ).readlines()
        )

    def get_jokes_data(self) -> dict:
        return self._load_json(f"{self.root_path}/data/jokes/data.json")

    def update_jokes_data(self, data: dict):
        with open(f"{self.root_path}/data/jokes/data.json", "w") as f:
            json.dump(data, f)

    def get_jokes(self) -> set:
        jokes = set()

        jokes_root = f"{self.root_path}/data/jokes/raw"
        for category in self._listdir(jokes_root):
            category_path = f"{jokes_root}/{category}"
            for filename in self._listdir(category_path):
                lines = []
                with open(f"{category_path}/{filename}", "r") as f:
                    for line in f.readlines():
                        lines.append(line.strip())
                jokes.add(tuple(lines))

        print(f"Obecna liczba żartów: {len(jokes)}.")
        return jokes

    def save_joke(self, joke_lines: list[str], category: str):
        save_dir = f"{self.root_path}/data/jokes/raw/{category}"
        if os.path.exists(save_dir) is False:
            os.mkdir(save_dir)
        n = len(self._listdir(save_dir))
        with open(f"{save_dir}/{n}.txt", "w") as f:
            for line in joke_lines:
                f.write(f"{line}\n")

    # YOUTUBE
    def get_youtube_data(self):
        return self._load_json(f"{self.root_path}/data/youtube/data.json")

    def update_videos_data(self, videos: list[dict]):
        dir_path = f"{self.root_path}/data/youtube"
        self._mkdir(dir_path)

        youtube_data_path = f"{dir_path}/data.json"
        youtube_data = self._load_json(f"{self.root_path}/data/youtube/data.json")
        if youtube_data is None:
            youtube_data = {}

        youtube_data["videos"] = videos

        with open(youtube_data_path, "w") as f:
            json.dump(youtube_data, f)

    @staticmethod
    def _load_json(path: str) -> dict:
        data = None
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
        return data

    @staticmethod
    def _mkdir(path: str):
        if os.path.exists(path) is False:
            os.mkdir(path)

    @staticmethod
    def _listdir(path: str, ignore_hidden: bool = True):
        return [
            n for n in os.listdir(path) if not n.startswith(".") or not ignore_hidden
        ]
