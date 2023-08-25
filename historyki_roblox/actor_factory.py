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

    def get_all(self, max_image_height):
        audio, images, text = [], [], []
        for interval in self.intervals:
            image_clip = mvp.ImageClip(interval.image_path)
            image_width, image_height = image_clip.size
            new_image_width = image_width * (max_image_height / image_height)
            image_clip = image_clip.resize((new_image_width, max_image_height))
            image_x, image_y = self.position.get_object_position(new_image_width, max_image_height)
            image_clip = image_clip.set_position(image_x, iamge_y).set_start(interval.start).set_duration(interval.duration)
            text.append(image_clip)

            name_clip = mvp.TextClip(self.character.name, fontsize=60, color='red', stroke_color='yellow', stroke_width=3, font=font)
            name_x = image_x + new_image_width * .5 - name_clip.size[0] * .5
            name_text_clip = name_text_clip.set_position((name_x, image_y)).set_start(start).set_duration(duration)
            text.append(name_text_clip)

            for start_time, text, audio_clip in interval.dialogues:
                audio_clip = audio_clip.set_start(start_time)
                audio.append(audio_clip)

    def get_images(self, font):
        images, text = [], []
        for interval in self.online_intervals:
            start, duration = interval.get_start_and_duration()
            image_clip = self.roblox_image.set_start(start).set_duration(duration)
            images.append(image_clip)

            name_text_clip = mvp.TextClip(self.character.name, fontsize=60, color='red', stroke_color='yellow', stroke_width=3, font=font)
            image_x, image_y = image_clip.pos(0)
            name_x = image_x + image_clip.size[0] * .5 - name_text_clip.size[0] * .5
            name_text_clip = name_text_clip.set_position((name_x, image_y)).set_start(start).set_duration(duration)
            text.append(name_text_clip)

        return images, text

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
