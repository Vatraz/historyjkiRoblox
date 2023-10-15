import jsons

from historyjki_roblox.character_factory import Character, CharacterFactory
from historyjki_roblox.resource_manager import ResourceManager
from historyjki_roblox.story.story import Story
from historyjki_roblox.story.story_parser import GptStoryParser


class HistoryjkaManager:
    def __init__(self, historyjka_name: str):
        self._story_parser = GptStoryParser()
        self._character_factory = CharacterFactory()

        self._historyjka_name = historyjka_name

        self._raw_story = ""
        self._characters = {}
        self._story = Story(scenario=[], actors=[])

        historyjka_data = ResourceManager().load_historyjka_data(historyjka_name)
        if historyjka_data:
            self._init_historyjka_from_saved_data(historyjka_data)

    def _init_historyjka_from_saved_data(self, historyjka_data: dict | None):
        self._raw_story = historyjka_data["raw_story"]
        self._characters = {
            n: Character.from_json(d) for n, d in historyjka_data["characters"].items()
        }
        self._story = Story.from_json(historyjka_data["parsed_story"])

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
                self._characters[ch_id] = self._character_factory.create_character(
                    name=ch_id
                )

    def _apply_characters_overrides(self, characters_overrides: dict) -> None:
        for character_override in characters_overrides:
            ch_id = character_override["name"]
            self._characters[ch_id].face_image = character_override["face_image"]
            self._characters[ch_id].skin_image = character_override["skin_image"]

    def get_historyjka_data(self):
        return {
            "parsed_story": jsons.dump(self._story),
            "characters": jsons.dump(self._characters),
            "raw_story": self._raw_story,
        }

    def _save(self):
        ResourceManager().save_historyjka_data(
            self._historyjka_name, self.get_historyjka_data()
        )

    def get_story(self):
        return self._story

    def get_characters(self):
        return self._characters
