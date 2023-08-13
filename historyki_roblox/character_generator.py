import json
import os
import random
from typing import NamedTuple, Optional

from historyki_roblox.oskarek_generator import OskarekGenerator

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))


class Character(NamedTuple):
    name: str
    gender: str
    voice: str
    image: str
    roblox_character: str


class CharacterGenerator:
    def __init__(self, oskarek_generator: Optional[OskarekGenerator] = None):
        self.oskarek_generator = oskarek_generator or OskarekGenerator()
        self.voices_data = self._load_voices()

    def _load_voices(self) -> list:
        with open('data/voices/voices.json', 'r') as f:
            voices = json.load(f)
        return voices['voices']

    def choose_voice(self, gender: str) -> str:
        return random.choice(tuple(filter(lambda x: x['ssmlGender'] == gender, self.voices_data)))['name']

    def choose_roblox_character(self, requested_gender: str) -> str:
        chosen_gender = 'f' if requested_gender == 'FEMALE' else 'm'
        list_of_characters = os.listdir(f'{ROOT_PATH}/data/characters')
        return random.choice([char for char in list_of_characters if chosen_gender in char])

    def generate_random_character(self, name: str) -> Character:
        gender = 'FEMALE' if name[-1] == 'a' else 'MALE'
        voice = self.choose_voice(gender)
        image = self.oskarek_generator.get_oskarek_from_openai(gender)
        roblox_character = self.choose_roblox_character(gender)
        return Character(name=name, gender=gender, voice=voice, roblox_character=roblox_character, image=image)
