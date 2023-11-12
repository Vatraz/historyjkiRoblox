from abc import ABC, abstractmethod

from historyjki_roblox.story.story import Story


class StoryParserBase(ABC):
    @abstractmethod
    def parse_raw_story(self, raw_story: str) -> Story:
        raise
