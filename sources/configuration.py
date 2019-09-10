import json
import os
from argparse import Namespace

configCommands = ["allowedTags", "interval", "repeat"]
modulChangeCommands = ["recognizer", "fetcher"]
appCommands = ["now", "set"]
supportedImageRecognizers = ["IntelNature"]
supportedImageFetchers = ["rWallpapers", "FromDirectory"]


class AppConfiguration:

    defaultJson = {
        "WallpaperSaveDirPath": r"/home/arkadiusz/Desktop/Projects/PythonBackground/project-ng2/SavedWallpapers/",
        "Interval": None,
        "Repeat": False,
        "FetcherConfigs": {
            "FromDirectory": {
                "Path": r"/home/arkadiusz/Desktop/Projects/PythonBackground/project_ng/"
            },
            "rWallpapers": {},
        },
        "RecognizerConfigs": {
            "IntelNature": {
                "Path": "/home/arkadiusz/Desktop/Projects/PythonBackground/project-ng2/kernels/IntelNature.h5",
                "AllowedTags": ["Mountain"],
                "SetThreshold": 0.7,
            }
        },
        "PickedRecognizer": "IntelNature",
        "PickedFetcher": "FromDirectory",
    }

    def __init__(self, commands):
        self._ConfigPath = "config.json"
        self.Instance = self._LoadConfig(self._ConfigPath)
        self.Invoke(commands)

    def _LoadConfig(self, configFileLocation):
        d = None
        if os.path.exists(configFileLocation):
            f = open(configFileLocation, "r")
            rd = f.read()
            if rd:
                try:
                    d = json.loads(rd, object_hook=lambda d: Namespace(**d))
                except expression as identifier:
                    d = self.LoadsDefault()
            else:
                d = self.LoadsDefault()
        else:
            d = self.LoadsDefault()

        di = vars(d)
        di["Fetcher"] = vars(di["FetcherConfigs"]).get(di.get("PickedFetcher"))
        di["Recognizer"] = vars(di["RecognizerConfigs"]).get(di.get("PickedRecognizer"))
        return Namespace(**di)

    def LoadsDefault(self):
        return json.loads(
            json.dumps(self.defaultJson, default=lambda o: vars(o)),
            object_hook=lambda d: Namespace(**d),
        )

    def WriteChanges(self):
        di = vars(self.Instance)
        di.pop("Fetcher")
        di.pop("Recognizer")
        json.dump(
            vars(self.Instance),
            open(self._ConfigPath, "w+"),
            default=lambda o: vars(o),
            indent=2,
        )

    def SetKey(self, key, value):
        d = vars(self.Instance)
        self._SetKeyRecur(d, key, value)

    def _SetKeyRecur(self, dic, key, value):
        for k, v in dic.items():
            key = key[0].upper() + key[1:]
            if type(v) == Namespace:
                self._SetKeyRecur(vars(v), key, value)
            if k == key:
                dic[k] = value
                return

    def Invoke(self, commands):
        for name, value in commands.items():
            if name in configCommands:
                self.SetKey(name, value)
            if name in modulChangeCommands:
                self.SetModule(name, value)

    def SetModule(self, moduleName, value):
        self._SetKeyRecur(
            vars(self.Instance), f"Picked{moduleName.capitalize()}", value
        )


class ArgsIntercepter:
    def __init__(self, args):
        argDict = vars(args)

        self.Config = self._ParseConfig(argDict)
        self.App = self._ParseApp(argDict)

    def _ParseApp(self, argDict):
        return {k: v for k, v in argDict.items() if k in appCommands}

    def _ParseConfig(self, argDict):
        return {
            k: v
            for k, v in argDict.items()
            if k in configCommands or k in modulChangeCommands
        }

