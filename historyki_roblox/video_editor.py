from moviepy.editor import *

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

class VideoGenerator:
    def edit_clip(self):
# Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
clip = VideoFileClip(f'{ROOT_PATH}/data/videos/what.mp4').subclip(2,3)

# Generate a text clip. You can customize the font, color, etc.
txt_clip = TextClip("What?",fontsize=70,color='white')

# Say that you want it to appear 10s at the center of the screen
txt_clip = txt_clip.set_pos('center').set_duration(1)

# Overlay the text clip on the first video clip
video = CompositeVideoClip([clip, txt_clip])

# Write the result to a file (many options available !)
video.write_videofile(f'{ROOT_PATH}/data/videos/what_edited.mp4')

print('ready')