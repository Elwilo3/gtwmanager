from pathlib import Path
import shutil
import subprocess
import psutil
import webview


class ModManager:
    def __init__(self):
        self.plugins_folder = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Get To Work\BepInEx\plugins")
        self.disabled_folder = self.plugins_folder.parent / "disabled"
        self.disabled_folder.mkdir(exist_ok=True)

        self.game_data_folder = Path(r"C:\Users\lools\AppData\LocalLow\Isto\Get To Work")

        self.split_categories_folder = self.game_data_folder / "split_categories"
        self.active_split_file = self.split_categories_folder / "active.txt"

        self.gold_split_file = self.game_data_folder / "gold_split_times.txt"
        self.best_split_file = self.game_data_folder / "best_split_times.txt"

        self.split_categories_folder.mkdir(exist_ok=True)

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

    def is_game_running(self):
        for process in psutil.process_iter(["name"]):
            if process.info["name"] == "Get To Work.exe":
                return True

        return False

    def launch_game(self):
        game_exe = self.plugins_folder.parent.parent / "Get To Work.exe"

        for process in psutil.process_iter(["name"]):
            if process.info["name"] == "Get To Work.exe":
                process.terminate()
                process.wait()

        subprocess.Popen([game_exe])

    def get_split_categories(self):
        return [folder.name for folder in self.split_categories_folder.iterdir() if folder.is_dir()]

    def get_active_split_category(self):
        if self.active_split_file.exists():
            return self.active_split_file.read_text()

        return None

    def save_active_split_category(self):
        active = self.get_active_split_category()

        if active is None:
            return

        category_folder = self.split_categories_folder / active

        shutil.copy2(self.gold_split_file, category_folder / "gold_split_times.txt")
        shutil.copy2(self.best_split_file, category_folder / "best_split_times.txt")

    def set_active_split_category(self, category_name):
        self.save_active_split_category()

        category_folder = self.split_categories_folder / category_name

        shutil.copy2(category_folder / "gold_split_times.txt", self.gold_split_file)
        shutil.copy2(category_folder / "best_split_times.txt", self.best_split_file)

        self.active_split_file.write_text(category_name)

    def add_split_category(self, category_name):
        category_folder = self.split_categories_folder / category_name
        category_folder.mkdir()

        shutil.copy2(self.gold_split_file, category_folder / "gold_split_times.txt")
        shutil.copy2(self.best_split_file, category_folder / "best_split_times.txt")

    def remove_split_category(self, category_name):
        if category_name == self.get_active_split_category():
            return

        category_folder = self.split_categories_folder / category_name
        shutil.rmtree(category_folder)


manager = ModManager()

webview.create_window(
    "GTW Manager",
    "frontend/index.html",
    js_api=manager
)

webview.start()