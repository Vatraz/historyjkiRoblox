import os

from PIL import Image
from rembg import remove


def remove_background():
    list_of_files = os.listdir('C:/Users/Janek/postacki/')
    name_of_file = 0

    for file in list_of_files:
        name_of_file += 1
        input_path = 'C:/Users/Janek/postacki/' + file
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_path = 'C:/Users/Janek/postacki_png/' + str(name_of_file) + '.png'
        output_image.save(output_path)


def random_string(n: int=8) -> str:
    return ''