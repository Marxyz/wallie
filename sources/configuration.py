import json
from argparse import Namespace

configCommands = ["allowedTags", "interval", "repeat"]
modulChangeCommands = ["recognizer", "fetcher"]
appCommands = ["now", "set"]
supportedImageRecognizers = ["IntelImagesRecognizer"]
supportedImageFetchers = ["rWallpapers", "FromDirectory"]


class AppConfiguration:

    defaultJsonSchema = {
        "WallpapersSaveDirPath": r"../SavedWallpapers/",
        "Interval": 90,
        "Repeat": False,
        "Fetcher": {"Type": "rWallpapers"},
        "Recognizer": {
            "Type": "IntelImagesRecognizer",
            "AllowedTags": [],
            "SetThreshold": 0.7,
        },
    }

    def __init__(self, commands):
        self._ConfigPath = "config.config"
        self.Instance = self._LoadConfigFile(self._ConfigPath)
        self.Invoke(commands)

    def _LoadConfigFile(self, configFileLocation):
        f = open(configFileLocation, "w+")
        if len(f.read()):
            return json.load(f)
        else:
            return json.loads(
                json.dumps(self.defaultJsonSchema, default=lambda o: vars(o)),
                object_hook=lambda d: Namespace(**d),
            )

    def WriteChanges(self):
        json.dump(
            vars(self.Instance), open(self._ConfigPath, "w+"), default=lambda o: vars(o)
        )

    def SetKey(self, key, value):
        d = vars(self.Instance)
        self._SetKeyRecurs(d, key, value)

    def _SetKeyRecurs(self, dic, key, value):
        for k, v in dic.items():
            if type(v) == dict:
                self._SetKeyRecurs(v, key, value)
            if k == key.capitalize():
                dic[key.capitalize()] = value
                return

    def Invoke(self, commands):
        for name, value in commands.items():
            if name in configCommands:
                self.SetKey(name, value)
            if name in modulChangeCommands:
                self.SetModule(name, value)

    def SetModule(self, moduleName, value):
        self.SetKey[moduleName]["Type"] = value


class ArgsIntercepter:
    def __init__(self, args):
        argDict = vars(args)

        self.Config = self._ParseConfig(argDict)
        self.App = self._ParseApp(argDict)

    def _ParseApp(self, argDict):
        return {k: v for k, v in argDict.items() if k in appCommands}

    def _ParseConfig(self, argDict):
        return {k: v for k, v in argDict.items() if k in configCommands}

