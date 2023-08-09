from moviepy.editor import *

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))


class VideoGenerator:
    def create_clip(self):
        ...
        #load background clip with and choose the length
        #add characters
        #add subtitles

    def load_background_clip(self, clip_length):
        ...

    def add_subtitles(self, text, corner):
        ...

    def add_character(self, picked_name):
        ...

    def add_name(self):
        ...

    def add_oskarek(self):
        ...

# Load video and select the subclip
clip = VideoFileClip(f'{ROOT_PATH}/data/videos/what.mp4').subclip(2,3)

# Generate a text clip. You can customize the font, color, etc.
txt_clip = TextClip("What?",fontsize=70,color='white')

# Say that you want it to appear 10s at the center of the screen
txt_clip = txt_clip.set_position(("center","top"))

# Overlay the text clip on the first video clip
video = CompositeVideoClip([clip, txt_clip])

# Write the result to a file (many options available !)
video.write_videofile(f'{ROOT_PATH}/data/videos/what_edited.mp4')

print('ready')