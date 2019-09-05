import sources.system
import os.path


class Application:
    def __init__(self, config, fetcher, recognizer):
        self.Commands = ["now", "set"]
        self.Fetcher = fetcher
        self.Recognizer = recognizer
        self.Config = config

    def Invoke(self, commands):

        for name, argument in commands.items():
            self.Commands[name](argument)

    def Now(self, arg):
        if not arg:
            return
        imageBatch = self.Fetcher.Get(config.FetchBatchSize)
        for img in imageBatch:
            labels = self.Recognizer.Recognize(img.Data)
            if (
                labels.First().Name in Config.Recognizer.AllowedTags
                and labels.First().Value > Config.Recognizer.SetThreshold
            ):
                path = sources.system.SaveImage(
                    os.path.join(config.WallpaperSaveDirPath, img.Name), img.Data
                )
                sources.system.SetWallpaper(path)

    def Set(self, arg):
        if not arg:
            return
        sources.system.SetWallpaper(arg)
