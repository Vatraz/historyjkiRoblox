from typing import NamedTuple

import cv2
import numpy as np

from historyjki_roblox.character_factory import Character
from historyjki_roblox.thumbnail.thumbnail_builder import ThumbnailBuilder


class ThumbnailDirector:
    def create_thumbnail_for_story(self, characters: list[Character]) -> np.ndarray:
        thumbnail_builder = ThumbnailBuilder()

        thumbnail = (
            thumbnail_builder.add_background()
            .add_characters(characters)
            .add_emoji()
            .add_thumbnail_phrase_random()
            .get_result()
        )

        return thumbnail


if __name__ == "__main__":
    # TEST
    class Character(NamedTuple):
        name: str
        gender: str
        voice: str
        image: str
        roblox_character: str

    characters = [
        Character(
            name="Robert",
            gender="MALE",
            voice="pl-PL-Wavenet-C",
            image="img",
            roblox_character="m20.png",
        ),
        Character(
            name="Bartosz",
            gender="MALE",
            voice="pl-PL-Standard-C",
            image="img",
            roblox_character="m49.png",
        ),
        Character(
            name="Oskar",
            gender="MALE",
            voice="pl-PL-Standard-C",
            image="img",
            roblox_character="m34.png",
        ),
        Character(
            name="PolishBoy",
            gender="MALE",
            voice="pl-PL-Standard-C",
            image="img",
            roblox_character="m62.png",
        ),
    ]
    cv2.imwrite("img.png", ThumbnailDirector().create_thumbnail_for_story(characters))
