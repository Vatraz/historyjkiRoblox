import eel
import jsons

from historyki_roblox.character_factory import CharacterFactory
from historyki_roblox.resource_manager import ResourceManager
from historyki_roblox.story.story import Story
from historyki_roblox.story.story_parser import GptStoryParser


class HistoryjkaEditor:
    def __init__(self, historyjka_name: str):
        self._story_parser = GptStoryParser()
        self._character_factory = CharacterFactory()

        self._historyjka_name = historyjka_name
        historyjka_data = ResourceManager().load_historyjka_data(historyjka_name)

        self._init_historyjka_from_saved_data(historyjka_data)

    def _init_historyjka_from_saved_data(self, historyjka_data: dict | None):
        if historyjka_data is None:
            self._raw_story = None
            self._characters = {}
            self._story = None
        else:
            self._raw_story = historyjka_data['raw_story']
            self._characters = historyjka_data['characters']
            self._story = Story.from_json(historyjka_data['parsed_story'])

    def update_story(self, raw_story: str, characters_overrides: dict, save=True):
        self._raw_story = raw_story
        self._story = self._story_parser.parse_raw_story(raw_story)
        self._update_saved_characters(self._story.actors)
        self._apply_characters_overrides(characters_overrides)

        if save:
            self._save()

    def _update_saved_characters(self, ids: list[str]) -> None:
        for ch_id in ids:
            if ch_id not in self._characters:
                self._characters[ch_id] = self._character_factory.create_random_character(name=ch_id)

    def _apply_characters_overrides(self, characters_overrides: dict) -> None:
        for character_override in characters_overrides:
            ch_id = character_override['name']
            self._characters[ch_id].face_image = character_override['face_image']
            self._characters[ch_id].skin_image = character_override['skin_image']

    def get_hisoryjka_data(self):
        return {
            "parsed_story": jsons.dump(self._story),
            "characters": jsons.dump(self._characters),
            "raw_story": self._raw_story
        }

    def _save(self):
        ResourceManager().save_historyjka_data(self._historyjka_name, self.get_hisoryjka_data())


historyjka_editor: HistoryjkaEditor | None = None


@eel.expose
def load_historyjka_editor(historyjka_name: str = 'default'):
    global historyjka_editor
    historyjka_editor = HistoryjkaEditor(historyjka_name)


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
    return ResourceManager().get_list_of_characters()


@eel.expose
def get_characters_faces():
    return ResourceManager().get_list_of_predefined_oskareks()


@eel.expose
def get_saved_stories():
    return ResourceManager().get_list_of_predefined_oskareks()


if __name__ == '__main__':
    load_historyjka_editor()
    eel.init("web")
    eel.start("editor.html")
