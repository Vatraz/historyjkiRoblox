import eel

from historyjki_roblox.historyjka_manager import HistoryjkaManager
from historyjki_roblox.resource_manager import ResourceManager
from historyjki_roblox.tasks.video_build_task_manager import (
    RobloxVideoBuilderManager,
    RobloxVideoBuilderManagerAlreadyInProgressException,
)

historyjka_manager: HistoryjkaManager | None = None
roblox_video_builder_manager: RobloxVideoBuilderManager | None = None


def _get_roblox_video_builder_manager() -> RobloxVideoBuilderManager:
    global roblox_video_builder_manager
    if not roblox_video_builder_manager:
        roblox_video_builder_manager = RobloxVideoBuilderManager()
    return roblox_video_builder_manager


@eel.expose
def load_historyjka_editor(historyjka_name: str = "default"):
    global historyjka_manager
    historyjka_manager = HistoryjkaManager(historyjka_name)
    return historyjka_manager.get_historyjka_data()


# EEL
@eel.expose
def parse_scenario(scenario_raw, characters_overrides=None):
    historyjka_manager.update_story(
        raw_story=scenario_raw, characters_overrides=characters_overrides
    )
    return historyjka_manager.get_historyjka_data()


@eel.expose
def create_story_copy(org_filename: str, dst_filename: str):
    return ResourceManager().copy_historyjka(org_filename, dst_filename)


@eel.expose
def remove_story(filename: str):
    return ResourceManager().remove_historyjka(filename)


@eel.expose
def get_characters_skins():
    return ResourceManager().get_list_of_characters()


@eel.expose
def get_characters_faces():
    return ResourceManager().get_list_of_predefined_oskareks()


@eel.expose
def get_saved_stories():
    return ResourceManager().get_saved_historyjkas()


@eel.expose
def render_video(historyjka_filename: str, video_params: dict):
    is_vertical = video_params["is_vertical"]
    video_name = video_params["video_name"]
    try:
        _get_roblox_video_builder_manager().spawn_video_build_task(
            historyjka_filename, video_name=video_name, is_vertical=is_vertical
        )
    except RobloxVideoBuilderManagerAlreadyInProgressException:
        return {
            "success": False,
            "msg": "Video building task already in progress",
        }
    except Exception as exe:
        return {
            "success": False,
            "msg": f"Unexpected error: {str(exe)}",
        }
    else:
        return {
            "success": True,
            "msg": "Video building task started",
        }


@eel.expose
def get_video_task_logs(historyjka_filename: str):
    return _get_roblox_video_builder_manager().get_task_logs(historyjka_filename)


@eel.expose
def get_video_task_liveness(historyjka_filename: str):
    return _get_roblox_video_builder_manager().is_task_alive(historyjka_filename)


if __name__ == "__main__":
    load_historyjka_editor()
    eel.init("web")
    eel.start("index.html")
