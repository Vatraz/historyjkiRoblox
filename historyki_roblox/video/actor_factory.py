import moviepy.editor as mvp
import random

from typing import Optional
from historyki_roblox.character_factory import Character, CharacterFactory
from historyki_roblox.resource_manager import ResourceManager
from historyki_roblox.video.video_position import Position, VideoSide


class VideoInterval:

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


class ActorVideoIntervalSet:
    def __init__(self, character: Character, position: Position, text_color: str):
        self.character = character
        self.position = position
        self.color = text_color
        self.is_online = False
        self.is_camera_on = False
        self.video_intervals = []
        self._resource_manager = ResourceManager()

    def add_dialogue(self, start, text, audio: mvp.AudioFileClip):
        self.video_intervals[-1].dialogues.append((start, text, audio))

    def end_current_interval(self, time: int):
        if len(self.video_intervals) != 0:
            self.video_intervals[-1].set_end(time)

    def join_room(self, time: int):
        self.is_online = True
        self.video_intervals.append(VideoInterval(time, self._resource_manager.get_roblox_character_path(self.character.skin_image)))
    
    def leave_room(self, time: int):
        self.is_online = False
        self.end_current_interval(time)

    def turn_on_camera(self, time: int):
        self.is_camera_on = True
        self.end_current_interval(time)
        self.video_intervals.append(VideoInterval(time, self._resource_manager.get_oskarek_path(self.character.face_image)))

    def turn_off_camera(self, time: int):
        self.is_camera_on = False
        self.end_current_interval(time)
        self.video_intervals.append(VideoInterval(time, self._resource_manager.get_roblox_character_path(self.character.skin_image)))

    def change_skin(self, time: int):
        self.end_current_interval(time)
        self.character.change_skin()
        self.video_intervals.append(VideoInterval(time, self._resource_manager.get_roblox_character_path(self.character.skin_image)))


class ActorVideoIntervalSetFactory:
    def __init__(self):
        self.character_factory = CharacterFactory()
        self.colors = ['yellow', 'violet', 'SkyBlue', 'HotPink', 'cyan', 'azure']

    def get_position(self, position_number: int) -> Position:
        x, y, side = 0, 0, None
        if position_number == 0:
            x, y, side = 0, .25, VideoSide.WEST
        elif position_number == 1:
            x, y, side = 1, .25, VideoSide.EAST
        elif position_number == 2:
            x, y, side = 0, .75, VideoSide.WEST
        elif position_number == 3:
            x, y, side = 1, .75, VideoSide.EAST
        elif position_number == 4:
            x, y, side = .5, .25, VideoSide.CENTER
        elif position_number == 5:
            x, y, side = .5, .75, VideoSide.CENTER
        return Position(x=x, y=y, side=side)

    def get_color(self) -> str:
        n = random.randint(0, len(self.colors) - 1)
        color = self.colors[n]
        self.colors.pop(n)
        return color

    def create_actor_interval_set(self, name: str, position_number: int, gender: Optional[str] = None, image: Optional[str] = None, roblox_image: Optional[str] = None) -> ActorVideoIntervalSet:
        character = self.character_factory.create_random_character(name, gender, image, roblox_image)
        position = self.get_position(position_number)
        text_color = self.get_color()
        return ActorVideoIntervalSet(character, position, text_color)