import json
import os
from pathlib import Path


class ResourceManager:

    def __init__(self):
        self.root_path = os.path.dirname(os.path.dirname(__file__))

    def get_list_of_characters(self):
        return os.listdir(f'{self.root_path}/data/characters')

    def get_prompts_data(self):
        with open(f'{self.root_path}/data/stories/prompts.json') as fp:
            prompts = json.load(fp)
        return prompts


print(ResourceManager().get_prompts_data)
