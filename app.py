import eel
import jsons

from historyki_roblox.character_factory import CharacterFactory, Character
from historyki_roblox.resource_manager import ResourceManager
from historyki_roblox.story.story import Story
from historyki_roblox.story.story_parser import GptStoryParser

story_parser = GptStoryParser()
resource_manager = ResourceManager()

CHARACTERS_CACHE: dict[str, Character] = {}


# "DB"
class HistoryjkaEditor:
    def __init__(self):
        self._story_parser = GptStoryParser()
        self._character_factory = CharacterFactory()

        self._raw_story: str | None = None
        self._characters: dict[str, Character] = {}
        self._story: Story | None = None
        self._story_id: str | None = None

    def update_story(self, raw_story: str, characters_overrides: dict):
        self._raw_story = raw_story
        self._story = self._story_parser.parse_raw_story(raw_story)
        self._update_saved_characters(self._story.actors)
        self._apply_characters_overrides(characters_overrides)

    def _apply_characters_overrides(self, characters_overrides: dict) -> None:
        for character_override in characters_overrides:
            ch_id = character_override['name']
            self._characters[ch_id].face_image = character_override['face_image']
            self._characters[ch_id].skin_image = character_override['skin_image']

    def _update_saved_characters(self, ids: list[str]) -> None:
        for ch_id in ids:
            if ch_id not in self._characters:
                self._characters[ch_id] = self._character_factory.create_random_character(name=ch_id)

    def get_hisoryjka_data(self):
        return {
            "parsed_story": jsons.dump(self._story),
            "characters": jsons.dump(self._get_characters_in_story(self._story.actors)),
            "raw_story": self._raw_story
        }

    def _get_characters_in_story(self, ids: list[str]) -> list[Character]:
        return [self._characters[ch_id] for ch_id in ids]


historyjka_editor = HistoryjkaEditor()


# EEL
@eel.expose
def parse_scenario(scenario_raw, characters_overrides=None):
    historyjka_editor.update_story(
        raw_story=scenario_raw,
        characters_overrides=characters_overrides
    )

    # TODO: this json could be our video generator input
    return historyjka_editor.get_hisoryjka_data()


@eel.expose
def get_characters_skins():
    return resource_manager.get_list_of_characters()


@eel.expose
def get_characters_faces():
    return resource_manager.get_list_of_predefined_oskareks()


@eel.expose
def get_saved_stories():
    return resource_manager.get_list_of_predefined_oskareks()


if __name__ == '__main__':
    eel.init("web")
    eel.start("editor.html")
