from enum import Enum
from typing import NamedTuple


class TaskState(Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    FAILED = "FAILED"


class TaskStatus:
    def __init__(
        self,
        task_status: TaskState = TaskState.NEW,
        error_info: str | None = None,
    ):
        self.task_status: TaskState = task_status
        self.error_info: str | None = error_info

    def update_status(self, new_status: TaskState):
        self.task_status = new_status

    def update_error_info(self, error_info: str):
        self.error_info = error_info

    def to_dict(self) -> dict:
        return dict(task_status=self.task_status.value, error_info=self.error_info)

    @classmethod
    def from_dict(cls, data: dict) -> "TaskStatus":
        return cls(
            task_status=TaskState[data["task_status"]], error_info=data["error_info"]
        )

    def is_task_in_not_terminal_state(self) -> bool:
        return self.task_status in [TaskState.NEW, TaskState.IN_PROGRESS]


class TaskStatusWithLog(NamedTuple):
    task_status: TaskStatus
    log: dict

    def to_dict(self):
        return {"task_status": self.task_status.to_dict(), "log": self.log}
