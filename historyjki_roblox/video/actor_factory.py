import random
from typing import Optional

from historyjki_roblox.character_factory import Character, CharacterFactory


class Interval:
    def __init__(self, start: int, image_path: str, position_number: int):
        self.start = start
        self.image_path = image_path
        self.position_number = position_number
        self.end = None
        self.duration = None
        self.dialogues = []

    def set_end(self, time: int):
        if self.end is None:
            self.duration = time - self.start
            self.end = time


class Actor:
    def __init__(
        self,
        character: Character,
        position_number: int,
        text_color: str,
        is_lector: bool,
    ):
        self.character = character
        self.position_number = position_number
        self.color = text_color
        self.is_lector = is_lector
        self.is_online = False
        self.is_camera_on = False
        self.intervals = []

    def set_position_number(self, number: int):
        self.position_number = number

    def add_dialogue(self, start: float, text: str, duration: float):
        if len(self.intervals) == 0:
            self.join_room(start)
        self.intervals[-1].dialogues.append((start, text, duration))

    def end_current_interval(self, time: int):
        if len(self.intervals) != 0:
            self.intervals[-1].set_end(time)

    def join_room(self, time: int):
        self.intervals.append(
            Interval(
                time,
                self.character.get_skin_image_path(),
                position_number=self.position_number,
            )
        )
        self.is_online = True

    def leave_room(self, time: int):
        self.end_current_interval(time)
        self.is_online = False

    def turn_on_camera(self, time: int):
        self.end_current_interval(time)
        self.intervals.append(
            Interval(
                time,
                self.character.get_face_image_path(),
                position_number=self.position_number,
            )
        )
        self.is_camera_on = True

    def turn_off_camera(self, time: int):
        self.is_camera_on = False
        self.end_current_interval(time)
        self.intervals.append(
            Interval(
                time,
                self.character.get_skin_image_path(),
                position_number=self.position_number,
            )
        )

    def change_skin(self, time: int):
        self.end_current_interval(time)
        self.character.change_skin()
        self.intervals.append(
            Interval(
                time,
                self.character.get_skin_image_path(),
                position_number=self.position_number,
            )
        )


class ActorVideoIntervalSetFactory:
    def __init__(self):
        self.character_factory = CharacterFactory()
        self.colors = [
            "AliceBlue",
            "SpringGreen4",
            "orchid2",
            "pink",
            "MintCream",
            "crimson",
        ]

    def get_color(self) -> str:
        n = random.randint(0, len(self.colors) - 1)
        color = self.colors[n]
        return color

    def create_actor(
        self,
        name: str,
        position_number: int,
        character: Optional[Character] = None,
        is_lector: bool = False,
    ) -> Actor:
        created_character = character
        if created_character is None:
            created_character = self.character_factory.create_character(name)

        text_color = self.get_color() if is_lector is False else "white"
        return Actor(created_character, position_number, text_color, is_lector)
