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

    def get_roblox_character(self, requested_gender: str) -> str:
        chosen_gender = 'f' if requested_gender == 'FEMALE' else 'm'
        chosen = random.choice([char for char in self.get_list_of_characters() if chosen_gender in char])
        return f'{self.root_path}/data/characters/{chosen}'

    # OSKAREK

    def get_list_of_oskareks(self):
        return os.listdir(f'{self.root_path}/output/oskareks')

    def save_oskarek_image(self, image: Image, image_name: str):
        return image.save(f'{self.root_path}/output/oskareks/{image_name}')

    def get_oskarek_image(self, requested_gender: str) -> str:
        chosen_gender = 'f' if requested_gender == 'FEMALE' else 'm'
        chosen = random.choice([char for char in self.get_list_of_oskareks() if chosen_gender == char[0]])
        return f'{self.root_path}/output/oskareks/{chosen}'

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
        return Image.open(random.choice(self.get_list_of_backgrounds()))

    # possible categories: WOW, LAUGH, SAD etc...
    def get_thumbnail_emoji(self, category: EmojiCategory):
        chosen_category = category.value
        chosen_emoji = random.choice([char for char in self.get_list_of_emoji() if chosen_category in char])
        return Image.open(chosen_emoji)

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
        video_name = self.get_random_string() + '.mp4'
        return f'{self.root_path}/output/video/{video_name}'

# print(random.choice(ResourceManager().get_list_of_backgrounds()))
