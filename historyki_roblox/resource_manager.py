import json
import os
from pathlib import Path

from PIL import ImageFont, Image


class ResourceManager:

    def __init__(self):
        self.root_path = os.path.dirname(os.path.dirname(__file__))

    def get_list_of_characters(self):
        return os.listdir(f'{self.root_path}/data/characters')

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


print(ResourceManager().get_list_of_characters())