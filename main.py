from pathlib import Path
import shutil
import subprocess
import psutil
import subprocess
import webview

class ModManager:
    def __init__(self):
        self.plugins_folder = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Get To Work\BepInEx\plugins")
        self.disabled_folder = self.plugins_folder.parent / "disabled"

        self.disabled_folder.mkdir(exist_ok=True)

    def get_mods(self):
        enabled = [mod.name for mod in self.plugins_folder.iterdir()]
        disabled = [mod.name for mod in self.disabled_folder.iterdir()]

        return enabled, disabled

    def disable_mod(self, mod_name):
        source = self.plugins_folder / mod_name
        destination = self.disabled_folder / mod_name

        shutil.move(source, destination)

    def enable_mod(self, mod_name):
        source = self.disabled_folder / mod_name
        destination = self.plugins_folder / mod_name

        shutil.move(source, destination)

    def launch_game(self):
        game_exe = self.plugins_folder.parent.parent / "Get To Work.exe"
        subprocess.Popen([game_exe])

    def is_game_running(self):
        for process in psutil.process_iter(["name"]):
            if process.info["name"] == "Get To Work.exe":
                return True
        return False

    # Opens the game if not running, if already open GTW and reopens it
    def launch_game(self):
        game_exe = self.plugins_folder.parent.parent / "Get To Work.exe"
        for process in psutil.process_iter(["name"]):
            if process.info["name"] == "Get To Work.exe":
                process.terminate()
                process.wait()
        subprocess.Popen([game_exe])



manager = ModManager()

webview.create_window(
    "GTW Manager",
    "frontend/index.html",
    js_api=manager
)

webview.start()