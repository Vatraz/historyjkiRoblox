from moviepy.editor import *

from historyki_roblox.story.story import Story, Dialogue
from historyki_roblox.story.story_parser import GptStoryParser

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))


class VideoGenerator:

    def generate_video(self, story: Story, used_clip):
        start_video = 0
        q = 2
        added_text = []
        added_image = []
        for scenario_element in story.scenario:
            text_line = scenario_element.content
            character = scenario_element.actor

            added_text.append(TextClip(text_line, font='Arial', fontsize=12, color='white')
                              .set_position("center")
                              .set_duration(len(text_line)/20).set_start(start_video))

            # added_image.append(ImageClip(character)
            #                    .set_position("top")
            #                    .set_duration(q-p).set_start(p))
            start_video += (len(text_line)/20 + 1)
            q += 2
        return CompositeVideoClip([used_clip] + added_text + added_image)

    def position(self, character):

        ...
#     def create_clip(self):
#         ...
#         #load background clip with and choose the length
#         #add characters
#         #add subtitles
#
#     def load_background_clip(self, clip_length):
#         return VideoFileClip(random.choice(os.listdir(f'{ROOT_PATH}/data/videos/'))).set_duration(clip_length)
#
#     def add_subtitles(self, text, corner):
#         ...
#
#     def add_character(self, picked_name):
#         ...
#
#     def add_name(self):
#         ...
#
#     def add_oskarek(self):
#         ...
#
# # Load video and select the subclip
# clip = VideoFileClip(f'{ROOT_PATH}/data/videos/what.mp4').subclip(2,3)
#
# # Generate a text clip. You can customize the font, color, etc.
# txt_clip = TextClip("What?",fontsize=70,color='white')
#
# # Say that you want it to appear 10s at the center of the screen
# txt_clip = txt_clip.set_position(("center","top"))
#
# # Overlay the text clip on the first video clip
# video = CompositeVideoClip([clip, txt_clip]).cutout
#
# # Write the result to a file (many options available !)
# video.write_videofile(f'{ROOT_PATH}/data/videos/what_edited.mp4')
#
# print('ready')


if __name__ == '__main__':
    size = (1000, 500)
    duration = 10
    color = (0, 0, 0)
    output = f'{ROOT_PATH}/data/videos/color.mp4'
    fps = 25
    clip = ColorClip(size, color, duration=duration)

    input = "".join(open("data/stories/test_data/0.txt").readlines())
    story = GptStoryParser().parse_raw_story(input)

    video = VideoGenerator().generate_video(story, clip)
    video.write_videofile(output, fps=fps)