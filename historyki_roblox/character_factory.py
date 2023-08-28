import json
import os
import random

from typing import NamedTuple, Optional

from historyki_roblox.oskarek_generator import OskarekGenerator
from historyki_roblox.resource_manager import ResourceManager

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))


class Character:

    def __init__(self, name: str, gender: str, voice: str, face_image_path: str, skin_image_path: str):
        self.name = name
        self.gender = gender
        self.voice = voice
        self.face_image_path = face_image_path
        self.skin_image_path = skin_image_path

    def change_skin(self):
        chosen = random.choice([char for char in os.listdir(f'{ROOT_PATH}/data/characters') if self.gender[0].lower() in char])
        self.skin_image_path = f'{ROOT_PATH}/data/characters/{chosen}'


class CharacterFactory:
    def __init__(self, oskarek_generator: Optional[OskarekGenerator] = None):
        self.oskarek_generator = oskarek_generator or OskarekGenerator()
        self.resource_manager = ResourceManager()
        # self.voices_data = self._load_voices()
        self.voices_data = ResourceManager().get_voices()

    # def _load_voices(self) -> list:
    #     with open('data/voices/voices.json', 'r') as f:
    #         voices = json.load(f)
    #     return voices['voices']

    def choose_voice(self, gender: str) -> str:
        return random.choice(tuple(filter(lambda x: x['ssmlGender'] == gender, self.voices_data)))['name']

    # def choose_roblox_character(self, requested_gender: str) -> str:
    #     chosen_gender = 'f' if requested_gender == 'FEMALE' else 'm'
    #     list_of_characters = self.resource_manager.get_list_of_characters()
    #     # list_of_characters = os.listdir(f'{ROOT_PATH}/data/characters')
    #     chosen = random.choice([char for char in list_of_characters if chosen_gender in char])
    #     return f'{ROOT_PATH}/data/characters/{chosen}'

    def create_random_character(self, name: str, gender: Optional[str] = None, image: Optional[str] = None) -> Character:
        if gender is None:
            gender = 'FEMALE' if name[-1] == 'a' else 'MALE'
        
        if image is None:
            image = self.oskarek_generator.get_oskarek_from_openai(gender)

        voice = self.choose_voice(gender)
        roblox_image_path = self.resource_manager.get_roblox_character(gender)
        # roblox_image_path = self.choose_roblox_character(gender)
        return Character(name=name, gender=gender, voice=voice, skin_image_path=roblox_image_path, face_image_path=image)
