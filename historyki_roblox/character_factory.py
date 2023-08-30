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
        self.voices_data = self.resource_manager.get_voices()

    def choose_voice(self, gender: str) -> str:
        return random.choice(tuple(filter(lambda x: x['ssmlGender'] == gender, self.voices_data)))['name']

    def create_random_character(self, name: str, gender: Optional[str] = None, image: Optional[str] = None) -> Character:
        if gender is None:
            gender = 'FEMALE' if name[-1] == 'a' else 'MALE'
        
        if image is None:
            image = self.oskarek_generator.get_oskarek_from_openai(gender)

        voice = self.choose_voice(gender)
        roblox_image_path = self.resource_manager.get_roblox_character(gender)
        return Character(name=name, gender=gender, voice=voice, skin_image_path=roblox_image_path, face_image_path=image)
