from historyjki_roblox.story.story import Dialogue, Didascalia, Event, Scenario, Story
from historyjki_roblox.story.story_parser_base import StoryParserBase


class DramaStoryParser(StoryParserBase):
    def parse_raw_story(self, raw_story: str) -> Story:
        story_lines = self._extract_stroy_lines(raw_story)

        scenario = []
        for line in story_lines:
            if self._is_line_dialogue(line):
                scenario.append(self._parse_line_to_dialogue(line))
            elif self._is_line_event(line):
                scenario.append(self._parse_line_to_event(line))
            else:
                scenario.append(self._parse_line_to_didascalia(line))

        actors = self._get_actors_from_scenario(scenario)

        return Story(scenario=scenario, actors=actors)

    def _extract_stroy_lines(self, raw_story: str) -> list[str]:
        story_lines = raw_story.split("\n")
        story_lines = [line for line in story_lines if line]
        return story_lines


if __name__ == "__main__":
    input = "".join(open("data/stories/test_data/3.txt").readlines())
    parsed_story = DramaStoryParser().parse_raw_story(input)
    print("done")