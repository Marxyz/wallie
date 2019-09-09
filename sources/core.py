import sources.system
import os.path


class Application:
    def __init__(self, config, fetcher, recognizer):
        self.Commands = {"now": self.Now, "set": self.Set}
        self.Fetcher = fetcher
        self.Recognizer = recognizer
        self.Config = config

    def Invoke(self, commands):
        for name, argument in commands.items():
            if argument:
                self.Commands[name](argument)

    def Now(self, arg):
        imageGen = self.Fetcher.Fetch()
        for img in imageGen:
            if self.Recognizer and self.Config.Recognizer.AllowedTags:
                label = self.Recognizer.Recognize(img.ProcessedData)

                if (
                    label[0] not in self.Config.Recognizer.AllowedTags
                    or label[1] < self.Config.Recognizer.SetThreshold
                ):
                    continue

            path = sources.system.SaveImage(
                os.path.join(self.Config.WallpaperSaveDirPath, img.Name), img.RawData
            )
            sources.system.SetWallpaper(path)
            break

    def Set(self, arg):
        sources.system.SetWallpaper(arg)
