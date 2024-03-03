from historyjki_roblox.youtube.youtube_manager import YoutubeManager
from historyjki_roblox.youtube.youtube_relayer import YoutubeRelayer

relayer = YoutubeRelayer()
data = relayer.get_videos_data(['VEci3oWKi90'])
print(data)

# manager = YoutubeManager()
# manager._download_videos_data()