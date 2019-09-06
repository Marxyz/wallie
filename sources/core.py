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
        imageGen = self.Fetcher.GetGenerator()
        for img in imageGen:
            labels = self.Recognizer.Recognize(img.Data)
            if (
                labels.First().Name in self.Config.Recognizer.AllowedTags
                and labels.First().Value > self.Config.Recognizer.SetThreshold
            ):
                path = sources.system.SaveImage(
                    os.path.join(self.Config.WallpaperSaveDirPath, img.Name), img.Data
                )
                sources.system.SetWallpaper(path)
                break

    def Set(self, arg):
        sources.system.SetWallpaper(arg)
