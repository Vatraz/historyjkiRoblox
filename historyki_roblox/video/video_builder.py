import moviepy.editor as mvp

from tqdm import tqdm
from typing import Dict, List, NamedTuple, Optional, Tuple, Union

from historyki_roblox.actor_factory import Actor, ActorFactory
from historyki_roblox.resource_manager import ResourceManager
from historyki_roblox.story.story import Dialogue, Event, Didascalia, Story
from historyki_roblox.story.story_parser import GptStoryParser
from historyki_roblox.voice_generator import VoiceGenerator


class VideoBuilder:

    def __init__(self):
        self.gpt_story_parser = GptStoryParser()

        self.clip = mvp.ColorClip(size=(1920, 1080))
        self.story = None

        self.actor_factory = ActorFactory()
        self.resource_manager = ResourceManager()
        self.voice_generator = VoiceGenerator()

        self.actors = []
        self.images = []
        self.text = []
        self.audio = []
        self.pause_duration = 1
        self.time = 0
        self.subscription_reminder = False

        self.lector_voice = 'pl-PL-Standard-E'
        self.font = 'data/fonts/Roboto-Black.ttf'


    def _load_clip(self, clip_source_path: str) -> mvp.VideoFileClip:
        return mvp.VideoFileClip(clip_source_path)

    def _load_story(self, story_source_path: str) -> Story:
        story_text = "".join(open(story_source_path).readlines())
        return self.gpt_story_parser.parse_raw_story(story_text)

    def _create_actors(self) -> Dict[str, Actor]:
        return {name: self.actor_factory.create_actor(name, index) for index, name in enumerate(self.story.actors)}

    def add_story(self, story_source_path: str, actors: List[Actor] = None):
        ...

    def add_background_video(self, clip_source_path: str):
        self.clip = mvp.VideoClip(clip_source_path)

    def get_looped_clip(self):
        return mvp.concatenate_videoclips([self.clip for _ in range(int(self.time / self.clip.duration) + 1)])

    def add_silent_pause(self):
        silence = mvp.AudioClip(make_frame=lambda t: [0], duration=self.pause_duration)
        self.audio.append(silence)
        self.time += self.pause_duration

    def add_text_with_voice_to_scene(self, text: str, voice: str, x: int, y: int, text_width: int, side: str='center', font_size: int=45, color: str='white'):
        self.add_silent_pause()
        audio_source_path = self.voice_generator.synthesize(text, voice)
        audio_clip = mvp.AudioFileClip(audio_source_path)
        text_clip = mvp.TextClip(
            text, 
            fontsize=font_size, 
            color=color, 
            stroke_color='black', 
            stroke_width=2, 
            font=self.font, 
            method='caption', 
            align=side, 
            size=(text_width, None)
        )
        text_width, text_height = text_clip.size
        text_y = y - text_height * .5
        text_x = x - text_width * .5
        if side == 'West':
            text_x = x
        elif side == 'East':
            text_x = x - text_width
        text_clip = text_clip.set_position((text_x, text_y)).set_start(self.time).set_duration(audio_clip.duration)

        self.audio.append(audio_clip)
        self.text.append(text_clip)
        self.time += audio_clip.duration

    def handle_event(self, event: Event):
        actor = self.actors[event.actor]
        if event.action == 'join room':
            actor.join_room(self.time)
        elif event.action == 'leave room':
            actor.leave_room(self.time)
        elif event.action == 'turn on camera':
            actor.turn_on_camera(self.time)
        elif event.action == 'turn off camera':
            actor.turn_off_camera(self.time)
        elif event.action == 'change skin':
            actor.change_skin(self.time)

    def handle_dialogue(self, dialogue: Dialogue):
        actor = self.actors[dialogue.actor]
        audio_source_path = self.voice_generator.synthesize(dialogue.content, actor.character.voice)
        audio_clip = mvp.AudioFileClip(audio_source_path).set_start(self.time)
        self.audio.append(audio_clip)

        actor.add_dialogue(self.time, dialogue.content, audio_clip)
        self.time += audio_clip.duration
        self.add_silent_pause()

    def lector(self, text: str):
        w, h = self.clip.size
        x = w * .5
        y = h * .5
        text_width = w * .75
        self.add_text_with_voice_to_scene(text, self.lector_voice, x, y, text_width, font_size=60)

    def get_object_position(self, x: int, y: int, width: int, height: int, side: str) -> Tuple[int, int]:
        pos_x = x * self.clip.size[0]
        pos_y = y * self.clip.size[1] - height * .5
        if side == 'East':
            pos_x -= width
        elif side == 'center':
            pos_x -= width * .5
        elif side == 'West':
            pass
        return pos_x, pos_y

    def add_image_to_scene(self, image_path: str, start: int, duration: int, x: int, y: int, side: str, max_height: Union[int, None]):
        image_clip = mvp.ImageClip(image_path)
        if max_height is not None:
            image_width, image_height = image_clip.size
            new_image_width = image_width * (max_height / image_height)
            image_clip = image_clip.resize((new_image_width, max_height))

        image_width, image_height = image_clip.size
        image_x, image_y = self.get_real_position(x, y, image_width, image_height, side)
        image_clip = image_clip.set_position((image_x, image_y)).set_start(start).set_duration(duration)
        self.images.append(image_clip)
        return image_x, image_y, image_width, image_height

    def add_text_to_scene(self, text: str, start: int, duration: int, x: int, y: int, side: str, font_size: int = 45, color: str = 'white', max_width: Union[int, None] = None):
        text_clip = mvp.TextClip(
            text,
            fontsize=font_size,
            color=color,
            stroke_color='black',
            stroke_width=3,
            font=self.font,
            method='caption',
            align=side,
            size=(max_width, None)
        )
        text_x, text_y = self.get_real_position(x, y, text_clip.size[0], text_clip.size[1], side)
        text_clip = text_clip.set_position((text_x, text_y)).set_start(start).set_duration(duration)
        self.text.append(text_clip)

    def montage(self):
        self.lector('No hejka brzdące, co tam u was słychać?\n Piszcie w komentarzach.\n Zmasakrujcie przycisk subskrypcji!!!')
        
        for actor in self.actors.values():
            actor.join_room(self.time)

        for scenario_element in self.story.scenario:

            if self.subscription_reminder is False and self.time > 60:
                self.lector('Dawaj subka, teraz.')
                self.lector('Widze że nie dałeś.')
                self.subscription_reminder = True
                
            if type(scenario_element) == Dialogue:
                self.handle_dialogue(scenario_element)
            elif type(scenario_element) == Event:
                self.handle_event(scenario_element)
            elif type(scenario_element) == Didascalia:
                ...

        self.lector('Hejka założyłam konto na instagramie i możecie wpaść tutaj i napisać w razie jakiś pytań.')

        for name, actor in self.actors.items():
            actor.leave_room(self.time)
            for i in actor.intervals:
                max_image_height = self.clip.size[1] * .4
                x, y, w, h = self.add_image_to_scene(i.image_path, i.start, i.duration, actor.position.x, actor.position.y, actor.position.side, max_image_height)
                name_x, name_y = x + w * .5, y
                self.add_text_to_scene(name, i.start, i.duration, name_x, name_y, 'center', 60, actor.color)

                text_x, text_y = 0, y + h * .5
                if actor.position.side == 'East':
                    text_x = x
                elif actor.position.side == 'center':
                    text_x = x + w * .5
                elif actor.position.side == 'West':
                    text_x = x + w

                text_width = self.clip.size[0] * .5
                for start, content, audio_clip in i.dialogues:
                    self.add_text_to_scene(content, start, audio_clip.duration, text_x, text_y, actor.position.side, color=actor.color, max_width=text_width)

    def save(self) -> str:
        looped_clip = self.get_looped_clip()
        video = mvp.CompositeVideoClip([looped_clip] + self.images + self.text).set_duration(self.time)
        video = video.set_duration(self.time)
        # video = video.set_duration(20)
 
        concated_audio = mvp.concatenate_audioclips(self.audio)
        video = video.set_audio(concated_audio)

        video_path = self.resource_manager.get_video_save_path()
        video.write_videofile(video_path)
        return video_path
