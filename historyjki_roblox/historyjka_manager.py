import jsons

from historyjki_roblox.character_factory import Character, CharacterFactory
from historyjki_roblox.resource_manager import ResourceManager
from historyjki_roblox.story.drama_story import DramaStoryParser
from historyjki_roblox.story.story import Story
from historyjki_roblox.story.story_parser_gpt import GptStoryParser


class HistoryjkaManager:
    def __init__(self, historyjka_name: str, raise_on_missing: bool = False):
        self._story_parser = DramaStoryParser()
        self._character_factory = CharacterFactory()

        self._historyjka_name = historyjka_name

        self._raw_story = ""
        self._characters: dict[str, Character] = {}
        self._story = Story(scenario=[], actors=[])

        historyjka_data = ResourceManager().load_historyjka_data(
            historyjka_name, raise_on_missing
        )
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
            character = self._characters[ch_id]

            character.face_image = character_override["face_image"]
            character.skin_image = character_override["skin_image"]

            if character.gender != character_override["gender"]:
                self._characters[ch_id] = self._character_factory.create_character(
                    name=character.name,
                    gender=character_override["gender"],
                    image=character.face_image,
                    roblox_image=character.skin_image,
                )

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

    def get_story(self) -> Story:
        return self._story

    def get_characters(self) -> dict[str, Character]:
        return self._characters

    def get_characters_list(self) -> list[Character]:
        return [
            character
            for character in self._characters.values()
            if character.name in self._story.actors
        ]
