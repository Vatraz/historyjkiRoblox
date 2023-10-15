import eel

from historyjki_roblox.historyjka_manager import HistoryjkaManager
from historyjki_roblox.resource_manager import ResourceManager

historyjka_manager: HistoryjkaManager | None = None


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


if __name__ == "__main__":
    load_historyjka_editor()
    eel.init("web")
    eel.start("index.html")
