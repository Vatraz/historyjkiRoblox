import eel
import jsons

from historyki_roblox.character_factory import CharacterFactory, Character
from historyki_roblox.resource_manager import ResourceManager
from historyki_roblox.story.story_parser import GptStoryParser

story_parser = GptStoryParser()
resource_manager = ResourceManager()
character_factory = CharacterFactory()

CHARACTERS_CACHE: dict[str, Character] = {}


# "DB"
def apply_characters_overrides(characters_overrides: dict) -> None:
    for character_override in characters_overrides:
        ch_id = character_override['name']
        CHARACTERS_CACHE[ch_id].face_image = character_override['face_image']
        CHARACTERS_CACHE[ch_id].skin_image = character_override['skin_image']


def update_saved_characters(ids: list[str]) -> None:
    for ch_id in ids:
        if ch_id not in CHARACTERS_CACHE:
            CHARACTERS_CACHE[ch_id] = character_factory.create_random_character(name=ch_id)


def get_saved_characters(ids: list[str]) -> list[Character]:
    return [CHARACTERS_CACHE[ch_id] for ch_id in ids]


# EEL
@eel.expose
def parse_scenario(scenario_raw, characters_overrides=None):
    parsed_story = story_parser.parse_raw_story(scenario_raw)

    update_saved_characters(parsed_story.actors)
    apply_characters_overrides(characters_overrides)
    characters = get_saved_characters(parsed_story.actors)

    # TODO: this json could be our video generator input
    return {
        "parsed_story": jsons.dump(parsed_story),
        "characters": jsons.dump(characters),
    }


@eel.expose
def get_characters_skins():
    return resource_manager.get_list_of_characters()


@eel.expose
def get_characters_faces():
    return resource_manager.get_list_of_predefined_oskareks()


if __name__ == '__main__':
    eel.init("web")
    eel.start("index.html")
