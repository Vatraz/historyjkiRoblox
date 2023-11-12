import json
import random
from typing import Optional

from historyjki_roblox.gpt_relayer import GtpRelayer
from historyjki_roblox.story.story import Story
from historyjki_roblox.story.story_parser_gpt import GptStoryParser


class StoryGenerator:
    def __init__(self, gpt_relayer: Optional[GtpRelayer] = None):
        self.gpt_relayer = gpt_relayer or GtpRelayer()
        self.gpt_story_parser = GptStoryParser()
        self.prompts_data = self._load_prompts_data()

    def _load_prompts_data(self):
        with open("data/stories/prompts.json") as fp:
            prompts = json.load(fp)
        return prompts

    def generate_story_predefined(self) -> Story:
        """
        Generate a story from a random predefined prompt using chat GPT
        """
        prompt = random.choice(self.prompts_data["prompts_basic"])
        raw_story = self.gpt_relayer.simply_ask(prompt)
        story = self.gpt_story_parser.parse_raw_story(raw_story)
        return story


if __name__ == "__main__":
    StoryGenerator().generate_story_predefined()
