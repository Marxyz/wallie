import sources.system


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
        for img in self.Fetcher.Fetch():
            if self.Config.Recognizer and self.Config.Recognizer.AllowedTags:
                label = self.Recognizer.Recognize(img.ProcessedData)
                print(f"{label.Description} -> {label.Confidence}")
                if (
                    label.Description not in self.Config.Recognizer.AllowedTags
                    or label.Confidence < self.Config.Recognizer.SetThreshold
                ):
                    continue

            path = sources.system.SaveImage(
                self.Config.WallpaperSaveDirPath, img.Name, img.RawData
            )
            sources.system.SetWallpaper(path)
            break

    def Set(self, arg):
        sources.system.SetWallpaper(arg)
