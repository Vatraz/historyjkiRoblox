import moviepy.editor as mpv

from typing import Tuple

from historyki_roblox.character_factory import Character


class Actor:
    def __init__(self, character: Character, face_image: mpv.ImageClip, roblox_image: mpv.ImageClip, side: str):
        self.character = character
        self.face_image = face_image
        self.roblox_image = roblox_image
        self.side = side
        self.is_online = False
        self.is_camera_on = False

    def speak(self, text: str, audio_source_path: str, font: str) -> Tuple[mpv.TextClip, mpv.AudioClip]:
        current_image = self.face_image if self.is_camera_on is True else self.roblox_image
        image_x, image_y = current_image.pos(0)
        image_width, image_height = current_image.size

        text_clip = mpv.TextClip(text, fontsize=45, color='yellow', stroke_color='black', stroke_width=1.75, font=font, method='caption', align=self.side, size=(800, None))
        text_width, text_height = text_clip.size

        text_x, text_y = 0, image_y + image_height * .5 - text_height * .5
        if self.side == 'West':
            text_x = image_x + image_width
        elif self.side == 'East':
            text_x = image_x - text_width

        text_clip = text_clip.set_position((text_x, text_y))

        audio_clip = mpv.AudioFileClip(audio_source_path)
        text_clip = text_clip.set_duration(audio_clip.duration)

        return text_clip, audio_clip

    def join_room(self):
        self.roblox_image.set_opacity(1)
        self.is_online = True
    
    def leave_room(self):
        self.roblox_image.set_opacity(0)
        self.is_online = False

    def turn_on_camera(self):
        self.roblox_image.set_opacity(0)
        self.face_image.set_opacity(1)
        self.is_camera_on = True

    def turn_off_camera(self):
        self.roblox_image.set_opacity(1)
        self.face_image.set_opacity(0)
        self.is_camera_on = False


class ActorFactory:
    def __init__(self, clip_width, clip_height):
        self.clip_width = clip_width
        self.clip_height = clip_height

    def create_image(self, image_source_path: str, position_number: int) -> mpv.ImageClip:
        if image_source_path is None:
            return None

        image_clip = mpv.ImageClip(image_source_path)
        image_clip = image_clip.resize((400, 400))

        image_width, image_height = image_clip.size
        print(image_width, image_height)

        image_x, image_y = 0, 0
        if position_number == 0:
            image_x = 0
            image_y = self.clip_height * .25 - image_height * .5
        elif position_number == 1:
            image_x = self.clip_width - image_width
            image_y = self.clip_height * .25 - image_height * .5
        elif position_number == 2:
            image_x = 0
            image_y = self.clip_height * .75 - image_height * .5
        elif position_number == 3:
            image_x = self.clip_width - image_width
            image_y = self.clip_height * .75 - image_height * .5

        image_clip = image_clip.set_position((image_x, image_y))
        return image_clip

    def create_actor(self, character: Character, position_number: int) -> Actor:
        roblox_image = self.create_image(character.roblox_image_path, position_number)
        face_image = self.create_image(character.face_image_path, position_number)
        side = 'West' if position_number % 2 == 0 else 'East'
        return Actor(character, face_image, roblox_image, side)
