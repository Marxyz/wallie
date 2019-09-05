import json

configCommands = ["tags", "interval", "repeat"]
appCommands = ["now", "set"]
supportedImageRecognizers = ["IntelImagesRecognizer"]
supportedImageFetchers = ["rWallpapers", "FromDirectory"]


class AppConfiguration:

    defaultJsonSchema = {
        "WallpapersSaveDirectoryPath": r"../SavedWallpapers/",
        "Interval": "",
        "Repeat": False,
        "Fetcher": {"Name":"rWallpapers", "BatchSize" : 2},
        "Recognizer": {"Name":"IntelImagesRecognizer", "AllowedTags" : [], "SetThreshold" : 0.7},
    }

    def __init__(self, commands):
        self.ConfigFile = "config.config"

    def _LoadConfigFile(self):
        j = json.load(self.ConfigFile)
        return j

    def _WriteConfigFile(self):
        json.dump(self.json, open(self.ConfigFile))


class ArgsIntercepter:
    def __init__(self, args):
        argDict = vars(args)
        self.Config = self._ParseConfig(argDict)
        self.App = self._ParseApp(argDict)
        self.Recognizer = self._ParseRecognizer(argsDict)
        self.Fetcher = self._ParseFetcher(argsDict)

    def _ParseApp(self, argDict):
        return {k: v for k, v in argDict.items() if k in appCommands}

    def _ParseConfig(self, argDict):
        return {k: v for k, v in argDict.items() if k in configCommands}

