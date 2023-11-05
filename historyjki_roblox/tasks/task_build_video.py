from multiprocessing.managers import DictProxy

from historyjki_roblox.logging.log_interceptor_multiprocessing import (
    MultiprocessingLogInterceptor,
)
from historyjki_roblox.tasks.task_status import TaskState, TaskStatus
from historyjki_roblox.video.video_builder import VideoBuilder


def video_builder_task(
    historyjka_filename: str,
    video_name: str | None,
    is_vertical: bool,
    task_status_dict: DictProxy,
    log_dict: DictProxy,
):
    log_interceptor = MultiprocessingLogInterceptor(log_dict, historyjka_filename)
    status = TaskStatus.from_dict(task_status_dict[historyjka_filename])

    status.update_status(TaskState.IN_PROGRESS)

    task_status_dict[historyjka_filename] = dict(
        task_status_dict[historyjka_filename], **status.to_dict()
    )

    try:
        video_builder = VideoBuilder(log_interceptor=log_interceptor)
        video_builder.build_video_from_json(
            historyjka_filename, is_video_horizontal=not is_vertical
        )
        video_builder.save(video_name=video_name)
    except Exception as exe:
        status.update_status(TaskState.FAILED)
        status.update_error_info(str(exe))
    else:
        status.update_status(TaskState.FINISHED)
    finally:
        task_status_dict[historyjka_filename] = dict(
            task_status_dict[historyjka_filename], **status.to_dict()
        )
