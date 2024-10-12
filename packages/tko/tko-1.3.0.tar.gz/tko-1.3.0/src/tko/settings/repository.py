from typing import Any, Dict, List
import os
import json
import urllib
from ..util.remote_url import RemoteUrl, Absolute
from tko.game.game import Game

languages_avaliable = ["c", "cpp", "py", "ts", "js", "java", "go"]

class Repository:
    CFG_FILE = "rep.json"
    LOG_FILE = "rep_log.csv"
    INDEX_FILE = "Readme.md"

    def __init__(self, folder: str):
        self.folder: str = folder
        self.data: Dict[str, Any] = {}
        self.game = Game()

    def load_game(self):
        self.game.parse_file(self.load_index_or_cache())
        return self

    def get_json_file(self) -> str:
        return os.path.join(self.folder, Repository.CFG_FILE)
    
    def get_log_file(self) -> str:
        return os.path.join(self.folder, Repository.LOG_FILE)
    
    def get_index_path(self) -> str:
        return os.path.join(self.folder, Repository.INDEX_FILE)

    def get_rep_dir(self) -> str:
        return self.folder

    def load_index_or_cache(self) -> str:
        file: str = self.get_local_file()
        url: str = self.get_remote_url()
        # arquivo existe e é local
        if file != "" and os.path.exists(file) and url == "":
            return file

        # arquivo não existe e é remoto
        if url != "" and (file == "" or not os.path.exists(file)):
            cache_file = self.get_index_path()
            os.makedirs(self.folder, exist_ok=True)
            ru = RemoteUrl(url)
            try:
                ru.download_absolute_to(cache_file)
            except urllib.error.URLError:
                print("fail: Não foi possível baixar o arquivo do repositório")
                if os.path.exists(cache_file):
                    print("Usando arquivo do cache")
                else:
                    raise Warning("fail: Arquivo do cache não encontrado")
            return cache_file

        raise ValueError("fail: arquivo não encontrado ou configurações inválidas para o repositório")

    __remote_url = "remote"  #remote url
    __local_file = "local"  #local file
    __expanded = "expanded"
    __new_items = "new_items"
    __tasks = "tasks"
    __flags = "flags"
    __lang = "lang"
    __selected = "index"

    defaults = {
        __remote_url: "",
        __local_file: "",
        __expanded: [],
        __tasks: {},
        __flags: {},
        __new_items: [],
        __lang: "",
        __selected: ""
    }

    def get_local_file(self) -> str:
        return self.__get(Repository.__local_file)
    
    def set_local_file(self, value: str):
        self.__set(Repository.__local_file, value)
        return self

    def get_remote_url(self) -> str:
        return self.__get(Repository.__remote_url)
    
    def set_remote_url(self, value: str):
        self.__set(Repository.__remote_url, value)
        return self

    def get_selected(self) -> str:
        return self.__get(Repository.__selected)

    def get_expanded(self) -> List[str]:
        return self.__get(Repository.__expanded)

    def get_new_items(self) -> List[str]:
        return self.__get(Repository.__new_items)
    
    def get_tasks(self) -> Dict[str, Any]:
        return self.__get(Repository.__tasks)
    
    def get_flags(self) -> Dict[str, Any]:
        return self.__get(Repository.__flags)
    
    def get_lang(self) -> str:
        return self.__get(Repository.__lang)

    def set_expanded(self, value: List[str]):
        return self.__set(Repository.__expanded, value)
    
    def set_new_items(self, value: List[str]):
        return self.__set(Repository.__new_items, value)
    
    def set_tasks(self, value: Dict[str, str]):
        self.__set(Repository.__tasks, value)
        return self
    
    def set_flags(self, value: Dict[str, Any]):
        self.__set(Repository.__flags, value)
        return self
    
    def set_lang(self, value: str):
        self.__set(Repository.__lang, value)
        return self
    
    def set_selected(self, value: str):
        self.__set(Repository.__selected, value)
        return self

    def __get(self, key: str) -> Any:
        if key not in self.defaults:
            raise ValueError(f"Key {key} not found in RepSettings")
        value = self.data.get(key, Repository.defaults[key])
        if type(value) != type(Repository.defaults[key]):
            return Repository.defaults[key]
        return value

    def __set(self, key: str, value: Any):
        self.data[key] = value
        return self

    def load_defaults(self):
        for key in Repository.defaults:
            self.data[key] = Repository.defaults[key]
        return self

    def load_data_from_json(self):
        if not os.path.exists(self.get_json_file()):
            print("Criando arquivo de configuração")
            self.load_defaults()
            if os.path.exists(self.get_index_path()):
                self.set_local_file(self.get_index_path())
            self.save_data_to_json()
            return self
        with open(self.get_json_file(), encoding="utf-8") as f:
            self.data = json.load(f)
        return self


    def save_data_to_json(self):
        json_file = self.get_json_file()
        if not os.path.exists(os.path.dirname(json_file)):
            os.makedirs(os.path.dirname(json_file))
        # filter keys that are not in defaults
        for key in list(self.data.keys()):
            if key not in Repository.defaults:
                del self.data[key]

        with open(json_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.data, indent=4))
        return self

    def __str__(self) -> str:
        return ( f"data: {self.data}\n" )
