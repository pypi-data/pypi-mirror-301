import json
from typing import Any, Dict
from .repository import Repository
from .app_settings import AppSettings
import os
import appdirs

from tko.util.text import Text
from tko.play.colors import Colors

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Settings:
    CFG_FILE = "settings.json"

    def __init__(self):
        self.remote: Dict[str, str] = {}
        self.reps: Dict[str, str] = {}
        self.app = AppSettings()
        self.colors = Colors()

        self.settings_file = ""

    def set_settings_file(self, path: str):
        self.settings_file = path
        return self

    def get_settings_file(self) -> str:
        if self.settings_file is None or self.settings_file == "":
            self.package_name = "tko"
            default_filename = self.CFG_FILE
            self.settings_file = os.path.abspath(default_filename)  # backup for replit, dont remove
            self.settings_file = os.path.join(appdirs.user_data_dir(self.package_name), default_filename)
        
        if not os.path.exists(self.settings_file):
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        return self.settings_file

    def reset(self):
        self.remote = {}
        self.remote["fup"] = "https://github.com/qxcodefup/arcade/blob/master/Readme.md"
        self.remote["ed"] = "https://github.com/qxcodeed/arcade/blob/master/Readme.md"
        self.remote["poo"] = "https://github.com/qxcodepoo/arcade/blob/master/Readme.md"
        self.reps = {}
        self.app = AppSettings()
        self.colors = Colors()
        return self

    def set_remote(self, alias: str, url_or_path: str):
        self.remote[alias] = url_or_path
        return self

    def get_remote(self, alias: str) -> str:
        if alias in self.remote:
            return self.remote[alias]
        raise Warning(f"Repositório {alias} não encontrado")

    def set_rep_folder(self, course: str, folder: str):
        self.reps[course] = folder
        return self
    
    def has_rep_folder(self, course: str) -> bool:
        return course in self.reps

    def get_rep_folder(self, course: str) -> str:
        if course in self.reps:
            folder = self.reps[course]
            if not isinstance(folder, str):
                self.reset()
                self.save_settings()
                return self.get_rep_folder(course)
            else:
                return folder
        raise Warning(f"Curso {course} não encontrado")
    
    def load_settings(self):
        try:
            settings_file = self.get_settings_file() # assure right loading if value == ""
            with open(settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.remote = data.get("remote", {})
                self.reps = data.get("reps", {})
                self.app = AppSettings().from_dict(data.get("geral", {}))
                self.colors = Colors().from_dict(data.get("colors", {}))
        except (FileNotFoundError, json.decoder.JSONDecodeError) as _e:
            self.reset()
            self.save_settings()
        return self

    # def check_rootdir(self):
    #     if self.app.get_rootdir() != "":
    #         return self
    #     print(Text().add("Pasta padrão para download de arquivos ").addf("r", "precisa").add(" ser definida."))
    #     here_cwd = os.getcwd()
    #     qxcode = os.path.join(os.path.expanduser("~"), "qxcode")

    #     while True:
    #         print(Text().addf("r", "1").add(" - ").add(here_cwd))
    #         print(Text().addf("r", "2").add(" - ").add(qxcode))
    #         print(Text().addf("r", "3").add(" - ").add("Outra pasta"))
    #         print(Text().add("Default ").addf("r", "1").add(": "), end="")
    #         op = input()
    #         if op == "":
    #             op = "1"
    #         if op == "1":
    #             home_qxcode = here_cwd
    #             break
    #         if op == "2":
    #             home_qxcode = qxcode
    #             break
    #         if op == "3":
    #             print(Text().addf("y", "Navegue até o diretório desejado e execute o tko novamente."))
    #             exit(1)

    #     if not os.path.exists(home_qxcode):
    #         os.makedirs(home_qxcode)
    #     print("Pasta padrão para download de arquivos foi definida em: " + home_qxcode)
    #     print(RawTerminal.centralize("", "-"))
    #     self.app._rootdir = home_qxcode
    #     self.save_settings();
    #     return self
    
    # def check_rep_alias(self, rep_alias: str):
    #     if rep_alias == "__ask":
    #         last = self.app.get_last_rep()
    #         if last != "" and last in self.remote:
    #             rep_alias = last
    #         else:
    #             print("Escolha um dos repositórios para abrir:")
    #             options: Dict[int, str] = {}
    #             for i, alias in enumerate(self.remote, start=1):
    #                 print(Text().addf("r", str(i)).add(f" - {alias}"))
    #                 options[i] = alias
    #             while True:
    #                 try:
    #                     print("Digite o número do repositório desejado: ", end="")
    #                     index = int(input())
    #                     if index in options:
    #                         rep_alias = options[index]
    #                         self.app.set_last_rep(rep_alias)
    #                         self.save_settings()
    #                         break
    #                 except ValueError:
    #                     pass
    #                 print("Digite um número válido")
    #     return rep_alias
    
    def save_settings(self):
        file = self.get_settings_file()
        value = {
            "remote": self.remote,
            "reps": self.reps,
            "geral": self.app.to_dict(),
            "colors": self.colors.to_dict()
        }
        with open(file, "w", encoding="utf-8") as f:
            json.dump(value, f, indent=4)
        return self

    # def __str__(self):
    #     output = ["Repositories:"]
    #     maxlen = max([len(key) for key in self.remote])
    #     for key in self.remote:
    #         prefix = f"- {key.ljust(maxlen)}"
    #         if self.remote[key].file and self.remote[key].url:
    #             output.append(f"{prefix} : dual   : {self.remote[key].url} ; {self.remote[key].file}")
    #         elif self.remote[key].url:
    #             output.append(f"{prefix} : remote : {self.remote[key].url}")
    #         else:
    #             output.append(f"{prefix} : local  : {self.remote[key].file}")
    #     return "\n".join(output)
