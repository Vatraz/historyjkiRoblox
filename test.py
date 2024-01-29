from historyjki_roblox.character_factory import CharacterFactory
from historyjki_roblox.story.story_parser_gpt import GptStoryParser
from historyjki_roblox.video.video_builder import VideoBuilder, HeadlessVideoBuilder

character_factory = CharacterFactory()
story_parser = GptStoryParser()

characters = []
for name in ['Baba', 'Lekarz']:
    character = character_factory.create_character(
        name=name
    )
    characters.append(character)

story_text = "".join(open("data/stories/test_data/0.txt", encoding="utf-8").readlines())
story = story_parser.parse_raw_story(story_text)

video_builder = HeadlessVideoBuilder()

video_builder.build_video(story=story, characters=characters, is_video_horizontal=False)
video_path = video_builder.save()
