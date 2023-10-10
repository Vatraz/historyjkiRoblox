import re

from historyjki_roblox.story.story import Story, Dialogue, Event, Scenario


class GptStoryParser:
    def parse_raw_story(self, raw_story: str) -> Story:
        story_lines = self._extract_stroy_lines(raw_story)

        scenario = []
        for line in story_lines:
            if self._is_line_dialogue(line):
                scenario.append(self._parse_line_to_dialogue(line))
            elif self._is_line_event(line):
                scenario.append(self._parse_line_to_event(line))

        actors = self._get_actors_from_scenario(scenario)

        return Story(scenario=scenario, actors=actors)

    def _extract_stroy_lines(self, raw_story: str) -> list[str]:
        story_lines = raw_story.split("\n")
        story_lines = [line for line in story_lines if line]
        return story_lines

    def _is_line_dialogue(self, line: str) -> bool:
        return not line.startswith(":") and ":" in line

    def _is_line_event(self, line: str) -> bool:
        return "=>" in line

    def _parse_line_to_dialogue(self, line: str) -> Dialogue:
        if "[" in line:
            emotion_match = re.search("\[.*\\]", line)
            content_raw = line[emotion_match.end() :]
            name_raw = line[: emotion_match.start()]

            emotion = emotion_match.group()[1:-1]
            name = name_raw.strip()
            content = " ".join(content_raw.split()[1:])
        else:
            name, content = line[: line.index(":")], line[line.index(":")+1 :]
            name, content = name.strip(), content.strip()
            emotion = None

        return Dialogue(content=content, actor=name, emotion=emotion)

    def _parse_line_to_event(self, line: str) -> Event:
        name, action = line.split("=>")
        return Event(actor=name.strip(), action=action.strip())

    def _get_actors_from_scenario(self, scenario: Scenario) -> list[str]:
        actors = list(
            set(
                scenario_element.actor
                for scenario_element in scenario
                if type(scenario_element) == Dialogue
            )
        )
        return actors


if __name__ == "__main__":
    input = "".join(open("data/stories/test_data/3.txt").readlines())
    parsed_story = GptStoryParser().parse_raw_story(input)
    print("done")
