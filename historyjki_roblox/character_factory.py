import random
from typing import Optional

from historyjki_roblox.oskarek_generator import OskarekGenerator
from historyjki_roblox.resource_manager import ResourceManager
from historyjki_roblox.voice_generator import Voice


class Character:
    def __init__(
        self, name: str, gender: str, voice: Voice, face_image: str, skin_image: str
    ):
        self.name = name
        self.gender = gender
        self.voice = voice
        self.face_image = face_image
        self.skin_image = skin_image

    def get_face_image_path(self):
        return ResourceManager().get_face_image_path(self.face_image)

    def get_skin_image_path(self):
        return ResourceManager().get_roblox_image_path(self.skin_image)

    def change_skin(self):
        self.skin_image = ResourceManager().get_random_roblox_character_name(
            self.gender
        )

    @classmethod
    def from_json(cls, data: dict) -> "Character":
        return Character(
            name=data.get("name"),
            gender=data.get("gender"),
            voice=Voice.from_json(data.get("voice")),
            face_image=data.get("face_image"),
            skin_image=data.get("skin_image"),
        )


class CharacterFactory:
    def __init__(self, oskarek_generator: Optional[OskarekGenerator] = None):
        self.oskarek_generator = oskarek_generator or OskarekGenerator()
        self.resource_manager = ResourceManager()
        self.voices_data = self.resource_manager.get_voices()

    def choose_voice(self, gender: str) -> Voice:
        # pitch = random.randint(-200, 200) * .1
        pitch = 0
        # speaking_rate = random.randint(250, 400) * .01
        speaking_rate = 1
        voice_name = random.choice(
            tuple(filter(lambda x: x["ssmlGender"] == gender, self.voices_data))
        )["name"]
        return Voice(name=voice_name, pitch=pitch, speaking_rate=speaking_rate)

    def create_character(
        self,
        name: str,
        gender: Optional[str] = None,
        image: Optional[str] = None,
        roblox_image: Optional[str] = None,
    ) -> Character:
        if gender is None:
            gender = "FEMALE" if name[-1] == "a" else "MALE"

        if image is None:
            image = "alien.png"

        voice = self.choose_voice(gender)

        if roblox_image is None:
            roblox_image = self.resource_manager.get_random_roblox_character_name(
                gender
            )

        return Character(
            name=name,
            gender=gender,
            voice=voice,
            skin_image=roblox_image,
            face_image=image,
        )
