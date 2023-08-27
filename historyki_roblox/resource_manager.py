import os
from pathlib import Path


class ResourceManager:

    def __init__(self):
        self.root_path = os.path.dirname(os.path.dirname(__file__))

    def get_list_of_characters(self):
        return os.listdir(f'{self.root_path}/data/characters')


print(ResourceManager().get_list_of_characters())
