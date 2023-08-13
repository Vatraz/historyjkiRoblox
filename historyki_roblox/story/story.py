from typing import NamedTuple, Optional, Union


class Didascalia(NamedTuple):
    content: str


class Dialogue(NamedTuple):
    content: str
    actor: str
    emotion: str


ScenarioElement = Union[Didascalia, Dialogue]
Scenario = list[ScenarioElement]


class Story(NamedTuple):
    scenario: Scenario
    actors: list[str]
    setting: Optional[str] = None
    summary: Optional[str] = None
