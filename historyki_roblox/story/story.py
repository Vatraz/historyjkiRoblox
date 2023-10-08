from typing import NamedTuple, Optional, Union


class Didascalia(NamedTuple):
    content: str


class Dialogue(NamedTuple):
    content: str
    actor: str
    emotion: str


class Event(NamedTuple):
    actor: str
    action: str


ScenarioElement = Union[Event, Didascalia, Dialogue]
Scenario = list[ScenarioElement]


class Story(NamedTuple):
    scenario: Scenario
    actors: list[str]
    setting: Optional[str] = None
    summary: Optional[str] = None

    @classmethod
    def from_json(cls, data: dict) -> "Story":
        scenario = []
        for scenario_elem_data in data["scenario"]:
            for scenario_elem_cls in ScenarioElement.__args__:
                if set(scenario_elem_data.keys()) == set(scenario_elem_cls._fields):
                    scenario.append(scenario_elem_cls(**scenario_elem_data))
                    break

        return cls(
            scenario=scenario,
            actors=data["actors"],
            setting=data["setting"],
            summary=data["summary"]
        )
