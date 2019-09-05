import json

configCommands = ["tags", "interval", "repeat"]
appCommands = ["now", "set"]
supportedImageRecognizers = ["IntelImagesRecognizer"]
supportedImageFetchers = ["rWallpapers", "FromDirectory"]


class AppConfiguration:

    defaultJsonSchema = {
        "WallpapersSaveDirPath": r"../SavedWallpapers/",
        "Interval": 90,
        "Repeat": False,
        "Fetcher": {"Name": "rWallpapers", "BatchSize": 2},
        "Recognizer": {
            "Name": "IntelImagesRecognizer",
            "AllowedTags": [],
            "SetThreshold": 0.7,
        },
    }

    def __init__(self, commands):
        self.ConfigFileLocation = "config.config"
        self._CurrentConfigFile = _LoadConfigFile()

    def _LoadConfigFile(self):
        j = json.load(self.ConfigFile)
        return j

    def WriteChanges(self):
        json.dump(self.json, open(self.ConfigFile))

    def __getattribute__(self, name):
        return self._CurrentConfigFile[name]


class ArgsIntercepter:
    def __init__(self, args):
        argDict = vars(args)
        self.Config = self._ParseConfig(argDict)
        self.App = self._ParseApp(argDict)

    def _ParseApp(self, argDict):
        return {k: v for k, v in argDict.items() if k in appCommands}

    def _ParseConfig(self, argDict):
        return {k: v for k, v in argDict.items() if k in configCommands}

