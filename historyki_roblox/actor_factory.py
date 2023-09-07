import moviepy.editor as mvp
import random

from typing import NamedTuple, Optional, Tuple, Union

from historyki_roblox.character_factory import Character, CharacterFactory


class Position(NamedTuple):
    x: float
    y: float
    side: str


class Interval:

    def __init__(self, start: int, image_path: str):
        self.start = start
        self.image_path = image_path
        self.end = None
        self.duration = None
        self.dialogues = []
    
    def set_end(self, time: int):
        if self.end is None:
            self.duration = time - self.start
            self.end = time


class Actor:

    def __init__(self, character: Character, position: Position, text_color: str):
        self.character = character
        self.position = position
        self.color = text_color
        self.is_online = False
        self.is_camera_on = False
        self.intervals = []

    def add_dialogue(self, start, text, audio: mvp.AudioFileClip):
        self.intervals[-1].dialogues.append((start, text, audio))

    def end_current_interval(self, time: int):
        if len(self.intervals) != 0: 
            self.intervals[-1].set_end(time)

    def join_room(self, time: int):
        self.is_online = True
        self.intervals.append(Interval(time, self.character.skin_image_path))
    
    def leave_room(self, time: int):
        self.is_online = False
        self.end_current_interval(time)

    def turn_on_camera(self, time: int):
        self.is_camera_on = True
        self.end_current_interval(time)
        self.intervals.append(Interval(time, self.character.face_image_path))

    def turn_off_camera(self, time: int):
        self.is_camera_on = False
        self.end_current_interval(time)
        self.intervals.append(Interval(time, self.character.skin_image_path))

    def change_skin(self, time: int):
        self.end_current_interval(time)
        self.character.change_skin()
        self.intervals.append(Interval(time, self.character.skin_image_path))


class ActorFactory:
    def __init__(self):
        self.character_factory = CharacterFactory()
        self.colors = ['yellow', 'violet', 'SkyBlue', 'HotPink', 'cyan', 'azure']

    def get_position(self, position_number: int) -> Position:
        x, y, side = 0, 0, None
        if position_number == 0:
            x, y, side = 0, .25, 'West'
        elif position_number == 1:
            x, y, side = .25, 'East'
        elif position_number == 2:
            x, y, side = 0, .75, 'West'
        elif position_number == 3:
            x, y, side = .75, 'East'
        elif position_number == 4:
            x, y, side = .5, .25, 'center'
        elif position_number == 5:
            x, y, side = .5, .75, 'center'
        return Position(x=x, y=y, side=side)

    def get_color(self) -> str:
        n = random.randint(0, len(self.colors) - 1)
        color = self.colors[n]
        self.colors.pop(n)
        return color

    def create_actor(self, name: str, position_number: int, gender: Optional[str] = None, image: Optional[str] = None) -> Actor:
        character = self.character_factory.create_random_character(name, gender, image)
        position = self.get_position(position_number)
        text_color = self.get_color()
        return Actor(character, position, text_color)
