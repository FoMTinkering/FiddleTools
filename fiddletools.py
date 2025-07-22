import json
import sys, os
from pathlib import Path
from dataclasses import dataclass
from typing import Mapping, Iterable

with open("settings.json") as fp:
    SETTINGS = json.load(fp)

def serialize_data(data: dict):
    """Turns a dict of the form
    ```
    {
    "A/B/C":"E",
    "A/B/D": "F",
    "G/H": "J",
    "G/I": "K"
    }
    ```
    into a dict of the form
    ```
    {
        "A": 
            {
                "B": {"C": "E", "D": "F"}
            }, 
        "G": {"H": "J", "I": "K"}
    }
    ```
    
    """
    new_dict = {}
    for key, val in data.items():
        d = new_dict
        while "/" in key:
            k = key[:key.find("/")]
            key = key[key.find("/")+1:]
            if k not in d:
                d[k] = {}
                d = d[k]
            else:
                if isinstance(d[k], dict):
                    d = d[k]
        d[key] = val
    return new_dict

class FiddleParser(Mapping):
    def __init__(
            self, 
            *,
            data:dict = None,
            path:str = SETTINGS["parser_settings"]["game_path"],
            filename:str = "__fiddle__", 
            is_open:bool = SETTINGS["parser_settings"]["is_open"],
            dark_mode:bool = SETTINGS["parser_settings"]["dark_mode"],
            filter:str = SETTINGS["parser_settings"]["filter"],
            serialize: bool = SETTINGS["parser_settings"]["serialize"]
    ):  
        """FiddleParser for Fields of Mistria game data. 
        Parses the `__fiddle__` file by default but can be used for other game JSONs.

        Args:
            data (dict, Optional): Raw data to be used for dict parsing. 
                If this is used, every other argument (except `filename`) will be ignored. Defaults to None.
            path (str, Optional): Path to the folder in which the file is. Defaults to what's written in the settings file.
            filename (str, Optional): Name of the file to be used. 
                A path to the file is also permitted but not recommended Defaults to `"__fiddle__"`.
            is_open (bool, Optional): Whether to open the list elements in the HTML output or not. Defaults to what's written in the settings file.
        
        """
        self.is_open = " open" if is_open else ""
        self.filename = Path(filename+".json")
        self.css = "fiddletools_dark" if dark_mode else "fiddletools"
        if data is None:
            self.path = path
            if not os.path.exists(self.path/Path(filename+".json")):
                raise ValueError("The file doesn't exist in the given directory.")
            with open(self.path/self.filename, encoding='utf-8') as fp:
                self.data = json.load(fp)
        else:
            self.data = data
        if serialize:
            self.data = serialize_data(self.data)
        self.serialize = serialize
        # we remove duplicate keys because the fiddle has a lot of redundancy... 
        # this is why make_details separates fsub and keys arguments
        f = filter
        match filter:
            case "slashes":
                f = lambda key : "/" not in key
            case "none":
                f = lambda key : True
        self.data_keys = [key for key in self.data if f(key)]
        

    def make_list(self, bullet:Iterable) -> str:
        """Makes an HTML list object out of the elements in the given `bullet` list.
        
        Args:
            bullet (Iterable): list of elements used to make the list.

        Returns:
            str: HTML string of the list output.
        """
        s = "<ul>"
        for el in bullet:
            s += "<li>"
            if isinstance(el, dict):
                if self.serialize:
                    el = serialize_data(el)
                s += self.make_details(el, list(el.keys()))
            elif isinstance(el, list):
                s += self.make_list(el)
            else:
                s += str(el)
            s += "</li>"
        s += "</ul>"
        return s

    def make_details(self, fsub:dict, keys:Iterable) -> str:
        """Makes an HTML defails object out of the elements in the given `fsub` dict and the keys from `keys`.
        The keys are generally just `list(fsub.keys())` but for practical purposes having two separate arguments 
        allows for more flexibility in the use of this method.
        
        Args:
            fsub (dict): dictionary to be used to make the HTML details elements.
            keys (Iterable): keys used to filter the dictionary.

        Returns:
            str: HTML string of the details output.
        """
        s = ""
        for key in keys:
            s += f"<details{self.is_open}><summary>{key}</summary>"
            bullet = fsub[key]
            if isinstance(bullet, dict):
                if self.serialize:
                    bullet = serialize_data(bullet)
                details = self.make_details(bullet, list(bullet.keys()))
            elif isinstance(bullet, list):
                details = self.make_list(bullet)
            else:
                details = f"<div>{str(bullet)}</div>"
            s += details
            s += "</details>"
        return s

    def to_html(self, *, output_folder:str = ""):
        """Exports FiddleParser object into a readable HTML file. 
        Filename will be the same as the FiddleParser filename (which defaults to `__fiddle__`).

        Args:
            output_folder (str, Optional): Folder in which the file will be saved. Defaults to `""`, which save to the local path.
        """
        self.html = f"""<head>
            <link rel="stylesheet" href="{self.css}.css">
        </head>
        <body>""" + (self.make_details(self.data, self.data_keys).encode("utf8").decode() if isinstance(self.data, dict) else self.make_list(self.data).encode("utf8").decode()) + "</body>"

        with open(Path(output_folder)/f"{self.filename.name[:-5]}.html", "w", encoding="utf-8") as fp:
            fp.write(self.html)

    def __str__(self):
        return str(self.data)
    def __len__(self):
        return len(self.data)
    def __getitem__(self, key):
        return self.data[key]
    def __iter__(self):
        return self.data.__iter__()
    

@dataclass
class FiddleComparator(Mapping):
    """FiddleComparator compares two fiddle files from different versions of Fields of Mistria.
    
    Args:
        path1 (str): Path to the first version. Defaults to what's written in the settings file.
        v1 (str): Name of the first version. Defaults to what's written in the settings file.
        path2 (str): Path to the second version. Defaults to what's written in the settings file.
        v2 (str): Name of the second version. Defaults to what's written in the settings file.
        output_folder (str): Folder in which output would be saved. Defaults to what's written in the settings file.
    """
    path1:str = SETTINGS["comparator_settings"]["v1"]["path"]
    v1:str = SETTINGS["comparator_settings"]["v1"]["version"]
    path2:str = SETTINGS["comparator_settings"]["v2"]["path"]
    v2:str = SETTINGS["comparator_settings"]["v2"]["version"]
    output_folder:str = SETTINGS["comparator_settings"]["output_folder"]
    filter:str = SETTINGS["comparator_settings"]["filter"]
    name:str = ""
    serialize: bool = SETTINGS["comparator_settings"]["serialize"]

    def find_differences(self, d1:dict, d2:dict):
        """Finds all differences between two dict objects.
        
        Args:
            d1 (dict): First dictionary.
            d2 (dict): Second dictionary.
            
        Returns:
            dict: Dictionary containing each key which is either not present in both versions, 
                or whose value is different between both versions. In either case, the name of 
                the version is used as a key to signal when something different is present, and 
                the value associated to it is the different value in question.
        """
        diff = {}
        for k in set(d1).intersection(d2):
            if isinstance(d1[k], dict) and d1[k] != d2[k]:
                diff[k] = self.find_differences(d1[k], d2[k])
            elif d1[k] != d2[k]:
                diff[k] = {self.v1:d1[k], self.v2:d2[k]}
        for k in set(d1).difference(d2):
            diff[k] = {self.v1:d1[k]}
        for k in set(d2).difference(d1):
            diff[k] = {self.v2:d2[k]}
        return diff

    @property
    def data(self):
        if not hasattr(self, "_data"):
            with open(self.path1, encoding='utf-8') as fp:
                f1 = json.load(fp)
            with open(self.path2, encoding='utf-8') as fp:
                f2 = json.load(fp)
            self._data = self.find_differences(f1,f2)
        return self._data

    @property
    def filename(self):
        return f"compare-{self.name}-_{self.v1}-{self.v2}"
    
    def to_html(self):
        """Exports the FiddleComparator object into a readable HTML file.
        Filename will be the same as the FiddleParser filename (which defaults to `__fiddle__`).
        """
        FiddleParser(
            data=self.data, 
            filename=self.filename,
            filter=self.filter,
            serialize=self.serialize
        ).to_html(output_folder=self.output_folder)

    def to_json(self):
        """Exports the FiddleComparator object into a JSON file.
        Filename will be the same as the FiddleParser filename (which defaults to `__fiddle__`).
        """
        with open(Path(self.output_folder)/f"{self.filename}.json", "w") as fp:
            json.dump(self.data, fp)

    def __str__(self):
        return str(self.data)
    def __len__(self):
        return len(self.data)
    def __getitem__(self, key):
        return self.data[key]
    def __iter__(self):
        return self.data.__iter__()