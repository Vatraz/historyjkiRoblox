import re

from historyjki_roblox.story.story import Dialogue, Didascalia, Event, Scenario, Story
from historyjki_roblox.story.story_parser_base import StoryParserBase


class DramaStoryParser(StoryParserBase):
    def parse_raw_story(self, raw_story: str) -> Story:
        story_lines = self._extract_story_lines(raw_story)

        scenario = []
        actors = []
        current_actor = None
        for line in story_lines:
            if self._is_line_actor(line):
                if line not in actors:
                    actors.append(line)
                current_actor = line
            elif self._should_skip_line(line):
                pass
            elif self._is_line_event(line):
                scenario.append(self._parse_line_to_event(line))
            else:
                scenario.append(self._parse_line_to_dialogue(line, current_actor))

        return Story(scenario=scenario, actors=actors)

    def _extract_story_lines(self, raw_story: str) -> list[str]:
        story_lines = raw_story.split("\n")
        story_lines = [line for line in story_lines if line]
        return story_lines

    def _is_line_actor(self, line: str) -> bool:
        return line.isupper()

    def _should_skip_line(self, line: str) -> bool:
        return line.startswith("/")

    def _is_line_event(self, line: str) -> bool:
        return "=>" in line

    def _parse_line_to_dialogue(self, line: str, actor: str) -> Dialogue:
        content = line.strip()
        name = actor
        emotion = None

        return Dialogue(content=content, actor=name, emotion=emotion)

    def _parse_line_to_event(self, line: str) -> Event:
        name, action = line.split("=>")
        return Event(actor=name.strip(), action=action.strip())


if __name__ == "__main__":
    input = "".join(open("data/stories/test_data/antygona.txt", encoding="utf8").readlines())
    parsed_story = DramaStoryParser().parse_raw_story(input)
    print("done")
