from historyki_roblox.story.story import Story, Dialogue
import re


class GptStoryParser:
    def parse_raw_story(self, raw_story: str) -> Story:
        story_lines = self._extract_stroy_lines(raw_story)

        scenario = []
        for line in story_lines:
            if self._is_line_dialogue(line):
                scenario.append(self._parse_line_to_dialogue(line))

        return Story(scenario=scenario)

    def _extract_stroy_lines(self, raw_story: str) -> list[str]:
        story_lines = raw_story.split("\n")
        story_lines = [line for line in story_lines if line]
        return story_lines

    def _is_line_dialogue(self, line: str) -> bool:
        return "[" in line and "]" in line and (("-") in line or ":" in line)

    def _parse_line_to_dialogue(self, line: str) -> Dialogue:
        emotion_match = re.search("\[.*\\]", line)
        content_raw = line[emotion_match.end() :]
        name_raw = line[: emotion_match.start()]

        emotion = emotion_match.group()[1:-1]
        name = name_raw.strip()
        content = " ".join(content_raw.split()[1:])

        return Dialogue(content=content, speaker=name, emotion=emotion)


if __name__ == "__main__":
    input = "".join(open("data/stories/test_data/0.txt").readlines())
    GptStoryParser().parse_raw_story(input)
