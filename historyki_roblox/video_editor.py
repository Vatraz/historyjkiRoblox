import os
import random

import numpy as np
import moviepy.editor as mpv

from typing import NamedTuple

from historyki_roblox.character_generator import Character, CharacterGenerator
from historyki_roblox.voice_generator import VoiceGenerator
from historyki_roblox.story.story import Story, Dialogue
from historyki_roblox.story.story_parser import GptStoryParser

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))


class Actor:
    def __init__(self, character: Character, face_image: mpv.ImageClip, roblox_image: mpv.ImageClip, side: str):
        self.character = character
        self.face_image = face_image
        self.roblox_image = roblox_image
        self.side = side
        self.is_online = False
        self.is_camera_on = False

    def speak(self, text: str, font: str) -> mpv.TextClip:
        current_image = self.face_image if self.is_camera_on is True else self.roblox_image
        image_x, image_y = current_image.pos(0)
        image_width, image_height = current_image.size

        text_clip = mpv.TextClip(text, fontsize=40, color='yellow', stroke_color='black', stroke_width=1.65, font=font, method='caption', align=self.side, size=(500, None))
        text_width, text_height = text_clip.size

        text_x, text_y = 0, image_y + image_height * .5 - text_height * .5
        if self.side == 'West':
            text_x = image_x + image_width
        elif self.side == 'East':
            text_x = image_x - text_width

        text_clip = text_clip.set_position((text_x, text_y))
        return text_clip

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


class ActorGenerator:
    def __init__(self, clip_width, clip_height):
        self.clip_width = clip_width
        self.clip_height = clip_height

    def create_image(self, image_source_path: str, position_number: int) -> mpv.ImageClip:
        if image_source_path is None:
            return None

        image_clip = mpv.ImageClip(image_source_path)

        image_width, image_height = image_clip.size

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

    def generate_actor(self, character: Character, position_number: int) -> Actor:
        roblox_image = self.create_image(character.roblox_image_path, position_number)
        face_image = self.create_image(character.face_image_path, position_number)
        side = 'West' if position_number % 2 == 0 else 'East'
        return Actor(character, face_image, roblox_image, side)


class VideoGenerator:

    def __init__(self):
        self.voice_generator = VoiceGenerator()
        self.character_generator = CharacterGenerator()
        self.font = '/usr/share/fonts/adobe-source-code-pro/SourceCodePro-Semibold.otf'
        self.pause_duration = .5

    def generate_video(self, story: Story, clip: mpv.VideoFileClip):
        clip_width, clip_height = clip.size
        actor_generator = ActorGenerator(clip_width, clip_height)

        actors = {}
        for c, name in enumerate(story.actors):
            generated_character = self.character_generator.generate_random_character(name)
            actors[name] = actor_generator.generate_actor(generated_character, c)

        clip_duration, added_text, added_sound = 0, [], []
        for scenario_element in story.scenario:
            actor = actors[scenario_element.actor]
            speech = self.voice_generator.synthesize(scenario_element.content, voice=actor.character.voice)

            audio_clip = mpv.AudioFileClip(speech.source_path)
            silent_audio = mpv.AudioClip(make_frame=lambda t: [0], duration=self.pause_duration)
            added_sound.append(audio_clip)
            added_sound.append(silent_audio)

            text_clip = actor.speak(scenario_element.content, self.font)
            text_clip = text_clip.set_start(clip_duration)
            text_clip = text_clip.set_duration(audio_clip.duration)
            added_text.append(text_clip)

            clip_duration += (speech.duration + self.pause_duration)

        added_images = []
        for _, actor in actors.items():
            image_clip = actor.roblox_image
            image_clip = image_clip.set_duration(clip_duration)
            added_images.append(image_clip)

        combined_audio = mpv.concatenate_audioclips(added_sound)

        video_loop = []
        for _ in range(int(combined_audio.duration / clip.duration) + 1):
            video_loop.append(clip)

        concatenated_loop = mpv.concatenate_videoclips(video_loop)
        video = mpv.CompositeVideoClip([concatenated_loop] + added_images + added_text)
        video = video.set_duration(combined_audio.duration)
        video = video.set_audio(combined_audio)
        return video
