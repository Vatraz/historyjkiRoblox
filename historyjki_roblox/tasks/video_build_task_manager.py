from multiprocessing import Manager, Process
from typing import NamedTuple

from historyjki_roblox.resource_manager import ResourceManager
from historyjki_roblox.tasks.task_build_video import video_builder_task
from historyjki_roblox.tasks.task_status import TaskState, TaskStatus, TaskStatusWithLog


class Params(NamedTuple):
    name: str | None = None
    is_vertical: bool = False


class RobloxVideoBuilderManager:
    def __init__(self):
        self._resource_manager = ResourceManager()
        self._tasks_statuses: dict[str:TaskState] = {}
        # self._tasks: dict[str: Process] = {}
        self._manager = Manager()
        self._tasks_statuses_dict = self._manager.dict()
        self._tasks_logs_dict = self._manager.dict()

    def spawn_video_build_task(self, historyjka_filename: str):
        if self._is_task_for_historyjka_in_progress(historyjka_filename):
            return "Historyjka video building task is in progress"
        print("Ok lets go")

        # init DictProxy for historyjka
        self._tasks_statuses_dict[historyjka_filename] = TaskStatus().to_dict()
        self._tasks_logs_dict[historyjka_filename] = {}

        p = Process(
            target=video_builder_task,
            args=(
                historyjka_filename,
                self._tasks_statuses_dict,
                self._tasks_logs_dict,
            ),
        )
        # TODO: Handle processes cleanup
        p.start()
        # p.join()

    def get_task_info(self, historyjka_filename: str) -> TaskStatusWithLog | None:
        try:
            return TaskStatusWithLog(
                task_status=self._tasks_statuses_dict[historyjka_filename],
                log=self._tasks_logs_dict[historyjka_filename],
            )
        except KeyError:
            return None

    def _is_task_for_historyjka_in_progress(self, historyjka_filename: str) -> bool:
        return (historyjka_filename in self._tasks_statuses_dict) and (
            TaskStatus.from_dict(
                self._tasks_statuses_dict[historyjka_filename]
            ).is_task_in_not_terminal_state()
        )
