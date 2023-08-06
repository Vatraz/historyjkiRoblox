from typing import NamedTuple, Optional, Union


class Didascalia(NamedTuple):
    content: str


class Dialogue(NamedTuple):
    speaker: str
    emotion: str


class Story(NamedTuple):
    scenario: list[Union[Didascalia, Dialogue]]
    setting: Optional[str] = None
    summary: Optional[str] = None
