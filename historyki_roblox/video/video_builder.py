import moviepy.editor as mvp

from typing import Dict, Tuple, Union

from historyki_roblox.video.actor_factory import ActorVideoIntervalSet, ActorVideoIntervalSetFactory
from historyki_roblox.resource_manager import ResourceManager
from historyki_roblox.story.actions import Action
from historyki_roblox.story.story import Dialogue, Event, Didascalia, Story
from historyki_roblox.story.story_parser import GptStoryParser
from historyki_roblox.video.video_position import VideoSide
from historyki_roblox.voice_generator import VoiceGenerator


class VideoBuilder:

    def __init__(self, story_source_path: str, actors: Dict[str, ActorVideoIntervalSet]):
        self.gpt_story_parser = GptStoryParser()
        self.actor_factory = ActorVideoIntervalSetFactory()
        self.resource_manager = ResourceManager()
        self.voice_generator = VoiceGenerator()

        self.clip = mvp.ColorClip(size=(1920, 1080), color=(0, 0, 0))
        self.story = self.load_story(story_source_path)
        self.actors = actors or self.create_actors()

        self.images = []
        self.text = []
        self.audio = []
        self.pause_duration = .95
        self.time = 0
        self.subscription_reminder = False

        self.lector_voice = 'pl-PL-Standard-E'
        self.font = 'data/fonts/Roboto-Black.ttf'


    def load_story(self, story_source_path: str) -> Story:
        story_text = "".join(open(story_source_path).readlines())
        return self.gpt_story_parser.parse_raw_story(story_text)

    def create_actors(self) -> Dict[str, ActorVideoIntervalSet]:
        return {name: self.actor_factory.create_actor_interval_set(name, index) for index, name in enumerate(self.story.actors)}

    def add_background_video(self, clip_source_path: str):
        self.clip = mvp.VideoFileClip(clip_source_path)

    def get_looped_clip(self):
        if isinstance(self.clip, mvp.ColorClip):
            self.clip = self.clip.set_duration(self.time)
            return self.clip
        return mvp.concatenate_videoclips([self.clip for _ in range(int(self.time / self.clip.duration) + 1)])

    def add_silent_pause(self):
        silence = mvp.AudioClip(make_frame=lambda t: [0], duration=self.pause_duration)
        self.audio.append(silence)
        self.time += self.pause_duration

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

    def handle_dialogue(self, dialogue: Dialogue):
        actor = self.actors[dialogue.actor]
        audio_source_path = self.voice_generator.synthesize(dialogue.content, actor.character.voice)
        audio_clip = mvp.AudioFileClip(audio_source_path).set_start(self.time)
        self.audio.append(audio_clip)

        actor.add_dialogue(self.time, dialogue.content, audio_clip)
        self.time += audio_clip.duration
        self.add_silent_pause()

    def lector(self, text: str):
        audio_source_path = self.voice_generator.synthesize(text, self.lector_voice)
        audio_clip = mvp.AudioFileClip(audio_source_path)
        self.audio.append(audio_clip)

        w, h = self.clip.size
        x = w * .5
        y = h * .5
        text_width = w * .8
        self.add_text_to_scene(text, self.time, audio_clip.duration, x, y, side=VideoSide.CENTER, font_size=60, max_width=text_width)
        self.time += audio_clip.duration
        self.add_silent_pause()

    def get_object_position(self, x: int, y: int, width: int, height: int, side: VideoSide) -> Tuple[int, int]:
        pos_x = x
        pos_y = y - height * .5
        if side == VideoSide.EAST:
            pos_x -= width
        elif side == VideoSide.CENTER:
            pos_x -= width * .5
        elif side == VideoSide.WEST:
            pass
        return pos_x, pos_y

    def add_image_to_scene(self, image_path: str, start: int, duration: int, x: int, y: int, side: VideoSide, max_height: Union[int, None]):
        image_clip = mvp.ImageClip(image_path)
        if max_height is not None:
            image_width, image_height = image_clip.size
            new_image_width = image_width * (max_height / image_height)
            image_clip = image_clip.resize((new_image_width, max_height))

        image_width, image_height = image_clip.size
        image_x, image_y = self.get_object_position(x, y, image_width, image_height, side)
        image_clip = image_clip.set_position((image_x, image_y)).set_start(start).set_duration(duration)
        self.images.append(image_clip)
        return image_x, image_y, image_width, image_height

    def add_text_to_scene(self, text: str, start: int, duration: int, x: int, y: int, side: VideoSide, font_size: int = 45, color: str = 'white', max_width: Union[int, None] = None):
        text_clip = mvp.TextClip(
            text,
            fontsize=font_size,
            color=color,
            stroke_color='black',
            stroke_width=3,
            font=self.font,
            method='caption',
            align=side.value,
            size=(max_width, None)
        )
        text_x, text_y = self.get_object_position(x, y, text_clip.size[0], text_clip.size[1], side)
        text_clip = text_clip.set_position((text_x, text_y)).set_start(start).set_duration(duration)
        self.text.append(text_clip)

    def add_sound(self, sound_file_path: str):
        audio_clip = mvp.AudioFileClip(sound_file_path)
        self.audio.append(audio_clip)
        self.time += audio_clip.duration

    def actor_join(self, actor: ActorVideoIntervalSet, is_sound: bool = False):
        actor.join_room(self.time)
        if is_sound is True:
            self.add_sound(self.resource_manager.get_discord_join_path())

    def actor_leave(self, actor: ActorVideoIntervalSet, is_sound: bool = True):
        actor.leave_room(self.time)
        if is_sound is True:
            self.add_sound(self.resource_manager.get_discord_join_path())

    def add_story_elements_to_video(self):
        for actor in self.actors.values():
            self.actor_join(actor, is_sound=False)

        for scenario_element in self.story.scenario:
            if type(scenario_element) == Dialogue:
                self.handle_dialogue(scenario_element)
            elif type(scenario_element) == Event:
                self.handle_event(scenario_element)
            elif type(scenario_element) == Didascalia:
                ...

        self.lector('Jeżeli macie ciekawe pomysły na nowe historyjki lub chcecie aby wasze imię znalazło sie w historyjce napiszcie o tym w komentarzu.')
        self.lector('Jeżeli wam się podobało nie zapomnijcie zostawić lajka pod filmikiem oraz subskrypcji na kanale.')

        for name, actor in self.actors.items():
            self.actor_leave(actor, is_sound=False)
            for i in actor.video_intervals:
                max_image_height = self.clip.size[1] * .4
                image_x = actor.position.x * self.clip.size[0]
                image_y = actor.position.y * self.clip.size[1]

                x, y, w, h = self.add_image_to_scene(i.image_path, i.start, i.duration, image_x, image_y, actor.position.side, max_image_height)
                name_x, name_y = x + w * .5, y
                self.add_text_to_scene(name, i.start, i.duration, name_x, name_y, VideoSide.CENTER, 60, actor.color)

                text_x, text_y = 0, y + h * .5
                if actor.position.side == VideoSide.EAST:
                    text_x = x
                elif actor.position.side == VideoSide.CENTER:
                    text_x = x + w * .5
                elif actor.position.side == VideoSide.WEST:
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
        video.write_videofile(video_path, fps=30)
        return video_path
