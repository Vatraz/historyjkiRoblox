from rembg import remove
from PIL import Image
import os
import random

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

class CharacterGenerator:
    def remove_background(self):
        list_of_files = os.listdir('C:/Users/Janek/postacki/')
        name_of_file = 0

        for file in list_of_files:
            name_of_file += 1
            input_path = 'C:/Users/Janek/postacki/' + file
            input_image = Image.open(input_path)
            output_image = remove(input_image)
            output_path = 'C:/Users/Janek/postacki_png/' + str(name_of_file) + '.png'
            output_image.save(output_path)

    def choose_character(self, requested_gender: str):
        chosen_gender = requested_gender
        list_of_characters = os.listdir(f'{ROOT_PATH}/data/characters')
        return random.choice([char for char in list_of_characters if chosen_gender in char])
