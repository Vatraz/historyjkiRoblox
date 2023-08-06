import os
import random

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))


class CharacterGenerator:
    def choose_character(self, requested_gender: str) -> str:
        chosen_gender = requested_gender
        list_of_characters = os.listdir(f'{ROOT_PATH}/data/characters')
        return random.choice([char for char in list_of_characters if chosen_gender in char])
