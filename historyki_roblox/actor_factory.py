import moviepy.editor as mvp

from typing import NamedTuple, Optional, Tuple, Union

from historyki_roblox.character_factory import Character, CharacterFactory


class Position(NamedTuple):
    x: int
    y: int
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

    def __init__(self, character: Character, position: Position):
        self.character = character
        self.position = position
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
    def __init__(self, clip_width, clip_height):
        self.clip_width = clip_width
        self.clip_height = clip_height
        self.character_factory = CharacterFactory()

    def get_position(self, position_number: int) -> Position:
        x, y, side = 0, 0, None
        if position_number == 0:
            x, y, side = 0, self.clip_height * .25, 'West'
        elif position_number == 1:
            x, y, side = self.clip_width, self.clip_height * .25, 'East'
        elif position_number == 2:
            x, y, side = 0, self.clip_height * .75, 'West'
        elif position_number == 3:
            x, y, side = self.clip_width, self.clip_height * .75, 'East'
        elif position_number == 4:
            x, y, side = self.clip_width * .5, self.clip_height * .25, 'center'
        elif position_number == 5:
            x, y, side = self.clip_width * .5, self.clip_height * .75, 'center'
        return Position(x=x, y=y, side=side)

    def create_actor(self, name: str, position_number: int, gender: Optional[str] = None, image: Optional[str] = None) -> Actor:
        character = self.character_factory.create_random_character(name, gender, image)
        position = self.get_position(position_number)
        return Actor(character, position)
