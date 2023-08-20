import os
import random

import moviepy.editor as mpv

from historyki_roblox.actor_factory import ActorFactory
from historyki_roblox.character_factory import CharacterFactory
from historyki_roblox.voice_generator import VoiceGenerator
from historyki_roblox.story.story import Story, Dialogue
from historyki_roblox.story.story_parser import GptStoryParser

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))


class VideoGenerator:

    def __init__(self):
        self.voice_generator = VoiceGenerator()
        self.character_factory = CharacterFactory()
        self.font = '/usr/share/fonts/adobe-source-code-pro/SourceCodePro-Semibold.otf'
        self.pause_duration = .5

    def get_silent_audio(self) -> mpv.AudioClip:
        return mpv.AudioClip(make_frame=lambda t: [0], duration=self.pause_duration)

    def generate_video(self, story: Story, clip: mpv.VideoFileClip):
        clip_width, clip_height = clip.size
        actor_factory = ActorFactory(clip_width, clip_height)

        actors = {}
        for c, name in enumerate(story.actors):
            created_character = self.character_factory.create_random_character(name)
            actors[name] = actor_factory.create_actor(created_character, c)

        clip_duration, added_text, added_sound = 0, [], []
        for scenario_element in story.scenario:
            actor = actors[scenario_element.actor]
            audio_source_path = self.voice_generator.synthesize(scenario_element.content, voice=actor.character.voice)

            text_clip, audio_clip = actor.speak(scenario_element.content, audio_source_path, self.font)
            text_clip = text_clip.set_start(clip_duration)

            added_text.append(text_clip)
            added_sound += [audio_clip, self.get_silent_audio()]

            clip_duration += (audio_clip.duration + self.pause_duration)

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
