import random
import moviepy.editor as mvp

from typing import Dict, List, Optional, Tuple

from historyjki_roblox.video.actor_factory import Actor, ActorVideoIntervalSetFactory
from historyjki_roblox.character_factory import Character
from historyjki_roblox.resource_manager import ResourceManager
from historyjki_roblox.story.actions import Action
from historyjki_roblox.story.story import Dialogue, Event, Didascalia, Story

from historyjki_roblox.voice_generator import VoiceGenerator


class VideoBuilder:

    def __init__(self, story: Story, is_video_horizontal: bool = True, characters: Optional[List[Character]] = None):
        self.actor_factory = ActorVideoIntervalSetFactory()
        self.resource_manager = ResourceManager()
        self.voice_generator = VoiceGenerator()

        self.story = story
        self.actors = self.create_actors(characters)

        self.audio = []
        self.images = []
        self.text = []
        self.clips = []
        self.clip_size = None
        self.is_video_horizontal = is_video_horizontal

        self.time = 0
        self.pause_duration = .5
        self.font = 'data/fonts/phrase.otf'

    def create_actors(self, characters: Optional[List[Character]]) -> Dict[str, Actor]:
        actors = {}

        if characters is not None:
            for index, character in enumerate(characters):
                print(character)
                actors[character.name] = self.actor_factory.create_actor(character.name, index, character=character)
        else:
            for index, name in enumerate(self.story.actors):
                actors[name] = self.actor_factory.create_actor(name, index)

        actors['lector'] = self.actor_factory.create_actor('lector', -1, is_lector=True)
        return actors
 
    def join_all(self, is_sound: bool = False):
        for actor in self.actors.values():
            self.actor_join(actor, is_sound=is_sound)

    def leave_all(self, is_sound: bool = False):
        for actor in self.actors.values():
            self.actor_leave(actor, is_sound=is_sound)

    def actor_join(self, actor: Actor, is_sound: bool = False):
        actor.join_room(self.time)
        if is_sound is True:
            self.add_sound(self.resource_manager.get_discord_join_path())

    def actor_leave(self, actor: Actor, is_sound: bool = True):
        actor.leave_room(self.time)
        if is_sound is True:
            self.add_sound(self.resource_manager.get_discord_join_path())

    def handle_event(self, event: Event):
        actor = self.actors[event.actor]
        if event.action == Action.JOIN_ROOM.value:
            self.actor_join(actor, is_sound=True)
        elif event.action == Action.LEAVE_ROOM.value:
            self.actor_leave(actor, is_sound=True)
        elif event.action == Action.TURN_ON_CAMERA.value:
            actor.turn_on_camera(self.time)
        elif event.action == Action.TURN_OFF_CAMERA.value:
            actor.turn_off_camera(self.time)
        elif event.action == Action.CHANGE_SKIN.value:
            actor.change_skin(self.time)

    def add_silent_pause(self, duration: Optional[int] = None):
        pause_duration = duration if duration is not None else self.pause_duration
        silence = mvp.AudioClip(make_frame=lambda t: [0], duration=pause_duration)
        self.audio.append(silence)
        self.time += self.pause_duration

    def add_sound(self, sound_file_path: str):
        audio_clip = mvp.AudioFileClip(sound_file_path)
        self.audio.append(audio_clip)
        self.time += audio_clip.duration

    def handle_dialogue(self, dialogue: Dialogue):
        actor = self.actors[dialogue.actor]
        print(dialogue.content, actor.character.voice)
        audio_source_path = self.voice_generator.synthesize(dialogue.content, actor.character.voice)
        audio_clip = mvp.AudioFileClip(audio_source_path).set_start(self.time)
        actor.add_dialogue(self.time, dialogue.content, audio_clip.duration)
        self.audio.append(audio_clip)
        self.time += audio_clip.duration
        self.add_silent_pause()

    def get_image_size(self, current_size: Tuple[int, int]) -> Tuple[int, int]:
        new_image_height = current_size[1]
        clip_width, clip_height = self.clip_size
        if clip_width >= clip_height:
            new_image_height = clip_height * .35
        elif clip_height > clip_width:
            new_image_height = clip_height * .19

        new_image_width = current_size[0] * (new_image_height / current_size[1])
        return new_image_width, new_image_height

    def get_text_side(self, position_number):

        if position_number < 0:
            return 'center'

        side = 'center'
        if self.is_video_horizontal is True:
            if position_number == 0 or position_number == 2:
                side = 'West'
            elif position_number == 1 or position_number == 3:
                side = 'East'
        elif self.is_video_horizontal is False:
            if position_number % 2 == 0:
                side = 'West'
            else:
                side = 'East' 

        return side

    def get_font_size_and_stroke_width(self) -> Tuple[int, int]:
        font_size = self.clip_size[0] // 30
        font_size = 50
        stroke_width = font_size // 30 + 1
        return font_size, stroke_width
 
    def get_dialogue_max_width(self):
        return self.clip_size[0] * 0.5

    def assign_story_elements(self):
        self.handle_dialogue(Dialogue(actor='lector', content='Zmasakrujcie przycisk subskrypcji.', emotion='spokój'))
        self.join_all()
        for scenario_element in self.story.scenario:
            if isinstance(scenario_element, Dialogue):
                self.handle_dialogue(scenario_element)
            elif type(scenario_element) == Event:
                self.handle_event(scenario_element)
            elif type(scenario_element) == Didascalia:
                ...
        self.leave_all()

    def set_name_position_based_on_image(self, position_number: int, text_clip: mvp.TextClip, image_clip: mvp.ImageClip) -> mvp.TextClip:

        # rotate text first
        if self.is_video_horizontal is False:
            if position_number == 4:
                text_clip = text_clip.rotate(89.99)
            elif position_number == 5:
                text_clip = text_clip.rotate(270)

        text_width, text_height = text_clip.size
        image_width, image_height = image_clip.size
        image_x, image_y = image_clip.pos(0)

        text_x, text_y = image_x + image_width * 0.5 - text_width * 0.5, 0
        if self.is_video_horizontal is True:
            if position_number == 0 or position_number == 1 or position_number == 4:
                text_y = image_y - text_height * 0.5
            elif position_number == 2 or position_number == 3 or position_number == 5:
                text_y = image_y + image_height - text_height * 0.5
        else:
            if position_number == 0 or position_number == 1:
                text_y = image_y - text_height * 0.5
            elif position_number == 2 or position_number == 3:
                text_y = image_y + image_height - text_height * 0.5
            elif position_number == 4:
                text_x = image_x - text_width * 0.5
                text_y = image_y + image_height * 0.5 - text_height * 0.5
            elif position_number == 5:
                text_x = image_x + image_width + text_width * 0.5
                text_y = image_y + image_height * 0.5 - text_height * 0.5

        text_x = max(min(text_x, self.clip_size[0] - text_width), 0)
        return text_clip.set_position((text_x, text_y))

    def set_text_position_based_on_image(self, position_number: int, text_side: str, text_clip: mvp.TextClip, image_clip: Optional[mvp.ImageClip] = None) -> mvp.TextClip:
        text_width, text_height = text_clip.size
        image_width, image_height = image_clip.size

        # if image_clip is
        image_x, image_y = image_clip.pos(0)

        if position_number == -1:
            return text_clip.set_position((image_x + image_width * 0.5 - text_width * 0.5, image_y + image_height * 0.5 - text_height * 0.5))

        text_x, text_y = 0, 0
        if text_side == 'West':
            text_x = image_x + image_width * 0.5
        elif text_side == 'East':
            text_x = image_x + image_width * 0.5 - text_width
        elif text_side == 'center':
            text_x = image_x + image_width * 0.5 - text_width * 0.5

        if position_number < 0:
            text_y = image_y - image_height * 0.5 - text_height * 0.5

        elif self.is_video_horizontal is True:
            if position_number == 0 or position_number == 1 or position_number == 4:
                text_y = image_y + image_height * 0.5
            elif position_number == 2 or position_number == 3 or position_number == 5:
                text_y = image_y + image_height * 0.5 - text_height
        else:
            if position_number == 0 or position_number == 1:
                text_y = image_y + image_height * 0.5
            elif position_number == 2 or position_number == 3:
                text_y = image_y + image_height * 0.5 - text_height
            elif position_number == 4 or position_number == 5:
                text_y = image_y + image_height * 0.5 - text_height * 0.5

        return text_clip.set_position((text_x, text_y))

    def get_image_position(self, position_number: int, image_width: int, image_height: int) -> Tuple[int, int]:
        clip_width, clip_height = self.clip_size
        if position_number < 0:
            # lector
            return clip_width * 0.5 - image_width * 0.5,  clip_height * 0.5 - image_height * 0.5

        x, y = 0, 0
        if clip_width > clip_height:
            if position_number in (0, 1, 4):
                y = clip_height * 0.25
            elif position_number in (2, 3, 5):
                y = clip_height * 0.75

            if position_number == 0 or position_number == 2:
                x = 0
            elif position_number == 1 or position_number == 3:
                x = clip_width - image_width
            elif position_number == 4 or position_number == 5:
                x = clip_width * 0.5 - image_width * 0.5

        else:
            if position_number % 2 == 0:
                x = 0
            elif position_number % 2 == 1:
                x = clip_width - image_width
            
            if position_number == 0 or position_number == 1:
                y = clip_height * 0.2
            elif position_number == 2 or position_number == 3:
                y = clip_height * 0.8
            elif position_number == 4 or position_number == 5:
                y = clip_height * 0.5

        y -= image_height * 0.5
        return x, y

    def add_actors_content(self):
        font_size, stroke_width = self.get_font_size_and_stroke_width()
        for name, actor in self.actors.items():
            for interval in actor.intervals:

                print(name, actor.character.name, interval.image_path)
                image_clip = mvp.ImageClip(interval.image_path)
                image_width, image_height = self.get_image_size(image_clip.size)
                image_clip = image_clip.resize((image_width, image_height))
                image_x, image_y = self.get_image_position(interval.position_number, image_width, image_height)
                image_clip = image_clip.set_start(interval.start).set_duration(interval.duration).set_position((image_x, image_y))

                if actor.is_lector is False:
                    name_text_clip = mvp.TextClip(name, fontsize=font_size+20, color=actor.color, stroke_color='black', stroke_width=stroke_width+1, font=self.font, method='caption')
                    name_text_clip = name_text_clip.set_start(interval.start).set_duration(interval.duration)
                    name_text_clip = self.set_name_position_based_on_image(interval.position_number, name_text_clip, image_clip)
                    self.images.append(image_clip)
                    self.text.append(name_text_clip)

                max_w = self.get_dialogue_max_width()
                for start, content, duration in interval.dialogues:
                    side = self.get_text_side(interval.position_number)
                    dialogue_text_clip = mvp.TextClip(content, fontsize=font_size, color=actor.color, stroke_color='black', stroke_width=stroke_width, font=self.font, method='caption', align=side, size=(max_w, None))
                    dialogue_text_clip = dialogue_text_clip.set_start(start).set_duration(duration)
                    dialogue_text_clip = self.set_text_position_based_on_image(interval.position_number, side, dialogue_text_clip, image_clip)
                    self.text.append(dialogue_text_clip)

    def add_background_video(self):
        # concat random downloaded
        videos = self.resource_manager.get_background_videos(is_horizontal=self.is_video_horizontal)
        x, y = (1920, 1080) if self.is_video_horizontal is True else (1080, 1920)

        if len(videos) == 0:
            color_clip = mvp.ColorClip(size=(x, y), color=(255, 0, 255)).set_duration(self.time)
            self.clips += [color_clip]
            self.clip_size = (x, y)
            return

        random.shuffle(videos)
        is_first, background_clips, total_duration = True, [], 0
        while self.time > total_duration:
            for video_path in videos:
                video_clip = mvp.VideoFileClip(video_path)
                video_clip = video_clip.resize((x, y))
                if is_first is True:
                    random_start_time = random.randint(0, int(video_clip.duration))
                    video_clip = video_clip.subclip(random_start_time)
                    is_first = False
                background_clips.append(video_clip)
                total_duration += video_clip.duration   
                if total_duration > self.time:
                    break
        
        concatenated = mvp.concatenate_videoclips(background_clips)
        self.clip_size = concatenated.size
        self.clips += [concatenated]

    def save(self) -> str:
        video = mvp.CompositeVideoClip(self.clips + self.images + self.text).set_duration(self.time)

        concated_audio = mvp.concatenate_audioclips(self.audio)
        video = video.set_audio(concated_audio)

        video_path = self.resource_manager.get_video_save_path()
        video.write_videofile(video_path, fps=30)
        return video_path
