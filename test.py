from historyjki_roblox.character_factory import CharacterFactory
from historyjki_roblox.story.story_parser import GptStoryParser
from historyjki_roblox.video.video_builder import VideoBuilder

character_factory = CharacterFactory()
story_parser = GptStoryParser()

characters_data = [
    ("Bartosz", "alien.png", "alien.png"),
    ("Robert", "robbcio.png", "m90.png"),
    ("Krystyna", "barbara.png", "f94.png"),
    ("Friz", "friz.jpg", "m45.png"),
]

characters = []
for name, image, roblox_image in characters_data:
    character = character_factory.create_character(
        name=name, image=image, roblox_image=roblox_image
    )
    characters.append(character)

story_text = "".join(open("data/stories/test_data/3.txt", encoding="utf-8").readlines())
story = story_parser.parse_raw_story(story_text)

video_builder = VideoBuilder()

video_builder.build_video(story=story, characters=characters, is_video_horizontal=False)
video_path = video_builder.save()
