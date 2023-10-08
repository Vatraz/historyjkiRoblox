import json
import os
import random
import string

from enum import Enum
from PIL import ImageFont, Image


class EmojiCategory(Enum):
    WOW = "w"


class ResourceManager:

    def __init__(self):
        self.root_path = os.path.dirname(os.path.dirname(__file__))

    # CHARACTER

    def get_list_of_characters(self):
        return os.listdir(f'{self.root_path}/data/characters')

    def get_random_roblox_character(self, requested_gender: str) -> str:
        chosen_gender = 'f' if requested_gender == 'FEMALE' else 'm'
        return random.choice([char for char in self.get_list_of_characters() if chosen_gender in char])

    def get_roblox_character_path(self, character_name: str) -> str:
        return f'{self.root_path}/data/characters/{character_name}'

    # OSKAREK

    def get_list_of_predefined_oskareks(self):
        return os.listdir(f'{self.root_path}/data/oskareks/images')

    def get_list_of_oskareks(self):
        return os.listdir(f'{self.root_path}/output/oskareks')

    def save_oskarek_image(self, image: Image, image_name: str):
        return image.save(f'{self.root_path}/output/oskareks/{image_name}')

    def get_random_oskarek_image_name(self, requested_gender: str) -> str:
        chosen_gender = 'f' if requested_gender == 'FEMALE' else 'm'
        return random.choice([char for char in self.get_list_of_oskareks() if chosen_gender == char[0]])

    def get_random_predefined_oskarek_image_name(self, requested_gender: str) -> str:
        chosen_gender = 'f' if requested_gender == 'FEMALE' else 'm'
        return random.choice([char for char in self.get_list_of_predefined_oskareks() if chosen_gender == char[0]])

    def get_oskarek_path(self, oskarek_name: str) -> str:
        if oskarek_name in self.get_list_of_predefined_oskareks():
            return f'{self.root_path}/data/oskareks/images/{oskarek_name}'
        else:
            return f'{self.root_path}/output/oskareks/{oskarek_name}'

    def get_face_image_path(self, image_name: str) -> str:
        return f'{self.root_path}/data/images/{image_name}'

    def get_roblox_image_path(self, image_name: str) -> str:
        return f'{self.root_path}/data/characters/{image_name}'

    # THUMBNAIL

    def get_list_of_backgrounds(self):
        return os.listdir(f'{self.root_path}/data/thumbnail/background')

    def get_list_of_emoji(self):
        return os.listdir(f'{self.root_path}/data/thumbnail/emoji')

    def get_thumbnail_data(self):
        with open(f"{self.root_path}/data/thumbnail/thumbnail_data.json") as fp:
            data = json.load(fp)
        return data

    def get_thumbnail_background(self):
        return Image.open(f'{self.root_path}/data/thumbnail/background/{random.choice(self.get_list_of_backgrounds())}')

    # possible categories: WOW, LAUGH, SAD etc...
    def get_thumbnail_emoji(self, category: EmojiCategory):
        chosen_category = category.value
        chosen_emoji = random.choice([char for char in self.get_list_of_emoji() if chosen_category in char])
        return Image.open(f'{self.root_path}/data/thumbnail/emoji/{chosen_emoji}')

    # OTHER

    def get_prompts_data(self):
        with open(f'{self.root_path}/data/stories/prompts.json') as fp:
            prompts = json.load(fp)
        return prompts

    def get_phrase_font(self):
        return ImageFont.truetype(
            f"{self.root_path}/data/fonts/phrase.otf", size=65
        )

    def get_voices(self) -> list:
        with open(f'{self.root_path}/data/voices/voices.json', 'r') as f:
            voices = json.load(f)
        return voices['voices']

    def get_gtts_api_key(self) -> str:
        return os.environ.get('GTTS_API_KEY')

    def get_random_string(self, length: int = 10) -> str:
        characters = string.ascii_letters + string.digits
        return ''.join([random.choice(characters) for _ in range(length)])

    def get_dialogue_path(self, dirname: str, text: str) -> str:
        filepath = f'{self.root_path}/output/dialogues/{dirname}'
        if os.path.exists(filepath) is False:
            os.mkdir(filepath)
        filename = text.lower().replace(' ', '_') + '.mp3'
        filepath = filepath + '/' + filename
        return filepath

    def get_video_save_path(self) -> str:
        if os.path.exists(f'{self.root_path}/output/video') is False:
            os.mkdir(f'{self.root_path}/output/video')
        video_name = self.get_random_string() + '.mp4'
        return f'{self.root_path}/output/video/{video_name}'

    def get_discord_join_path(self) -> str:
        return f'{self.root_path}/data/sounds/discord_join.mp3'

    def get_discord_leave_path(self) -> str:
        return f'{self.root_path}/data/sounds/discord_leave.mp3'

    def get_background_videos(self, is_horizontal: bool = True) -> list[str]:
        last_dir = 'horizontal' if is_horizontal is True else 'vertical'
        videos_dir = f'{self.root_path}/data/videos/{last_dir}'
        return [f'{videos_dir}/{i}' for i in os.listdir(videos_dir)]

# print(random.choice(ResourceManager().get_list_of_backgrounds()))
