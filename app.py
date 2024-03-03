import base64
import eel
import os

from historyjki_roblox.historyjka_manager import HistoryjkaManager
from historyjki_roblox.jokes.jokes_manager import JokesManager
from historyjki_roblox.resource_manager import ResourceManager
from historyjki_roblox.tasks.video_build_task_manager import (
    RobloxVideoBuilderManager,
    RobloxVideoBuilderManagerAlreadyInProgressException,
)

historyjka_manager: HistoryjkaManager | None = None
roblox_video_builder_manager: RobloxVideoBuilderManager | None = None

eel.init("web")

jokes_manager = JokesManager()


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


@eel.expose
def get_jokes_data():
    return jokes_manager._get_data()


@eel.expose
def get_joke_detail(joke_id: str):
    return jokes_manager._get_joke_data(joke_id)


@eel.expose
def get_jokes_categories():
    return jokes_manager._get_categories()


@eel.expose
def get_available_jokes_for_category(category: str):
    return jokes_manager._get_available_jokes_for_category(category)


@eel.expose
def get_joke_raw(category, filename):
    return ResourceManager().get_joke_raw(category, filename)


@eel.expose
def parse_joke(category, filename):
    return jokes_manager._parse_joke(category, filename)


@eel.expose
def add_new_joke(category: str, filename: str, title: str, parsed_text: str) -> bool:
    jokes_manager._add_joke(category, filename, title, parsed_text)


@eel.expose
def delete_joke(joke_id: str):
    jokes_manager._delete_joke(joke_id)


@eel.expose
def render_joke_video(joke_id: str):
    try:
        _get_roblox_video_builder_manager().spawn_joke_video_build_task(
            joke_id=joke_id
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
def upload_joke(joke_id: str, status: str, publish_time: str | None):
    video_id, video_data = jokes_manager._upload_joke(joke_id, status, publish_time)
    return {"videoId": video_id, "youtube": video_data}


@eel.expose
def delete_joke_video(joke_id: str):
    jokes_manager._delete_joke_video(joke_id)


@eel.expose
def get_video_base64(video_id: str):
    with open(f"output/video/{video_id}.mp4", 'rb') as video_file:
        encoded_string = base64.b64encode(video_file.read()).decode('utf-8')
    return f'data:video/mp4;base64,{encoded_string}'


if __name__ == "__main__":
    load_historyjka_editor()
    eel.start("index.html")
