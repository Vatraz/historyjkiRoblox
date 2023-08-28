import json
import os
import random
from pathlib import Path

from PIL import ImageFont, Image


class ResourceManager:

    def __init__(self):
        self.root_path = os.path.dirname(os.path.dirname(__file__))
        self.resource_manager = ResourceManager()

    def get_list_of_characters(self):
        return os.listdir(f'{self.root_path}/data/characters')

    def get_roblox_character(self, requested_gender: str) -> str:
        chosen_gender = 'f' if requested_gender == 'FEMALE' else 'm'
        chosen = random.choice([char for char in self.get_list_of_characters() if chosen_gender in char])
        return f'{self.root_path}/data/characters/{chosen}'

    def get_prompts_data(self):
        with open(f'{self.root_path}/data/stories/prompts.json') as fp:
            prompts = json.load(fp)
        return prompts

    def get_thumbnail_data(self):
        with open(f"{self.root_path}/data/thumbnail/thumbnail_data.json") as fp:
            data = json.load(fp)
        return data

    def get_phrase_font(self):
        return ImageFont.truetype(
            f"{self.root_path}/data/fonts/phrase.otf", size=65
        )

    def save_oskarek_image(self, image: Image, image_name: str):
        return image.save(f'{self.root_path}/data/oskareks/{image_name}')

    def get_voices(self) -> list:
        with open(f'{self.root_path}/data/voices/voices.json', 'r') as f:
            voices = json.load(f)
        return voices['voices']


print(ResourceManager().get_list_of_characters())
