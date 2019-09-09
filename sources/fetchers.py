import os
import PIL.Image
import random
import numpy


class rWallpapers:
    def __init__(self):
        pass

    def Fetch(self):
        pass


class FromDirectory:
    def __init__(self, dirEnumerate):
        random.shuffle(dirEnumerate)
        self.DirContents = dirEnumerate

    def Fetch(self):
        return self._CreateGen(self.DirContents, self.Projection, self.Limiter)

    def _CreateGen(self, elements, projectionFunc, limiter):
        return ImageGen(elements, projectionFunc, limiter)

    def Limiter(self, imagePath):
        return imagePath.split(os.extsep)[1] in ["jpg"]

    def Projection(self, imagePath):
        name = os.path.split(imagePath)[1]
        image = PIL.Image.open(imagePath)
        res_image = image.resize((150, 150))
        rawdata = numpy.asarray(image)
        data = numpy.asarray(res_image)
        return FetchedImage(name, data, rawdata)

    @classmethod
    def FromPath(cls, path):
        elements = [os.path.join(path, i) for i in os.listdir(path)]
        return FromDirectory(elements)


class ImageGen:
    def __init__(self, source, projection, limiter):
        self.Source = source
        self.Projection = projection
        self.Limiter = limiter

    def __iter__(self):
        for s in self.Source:
            if self.Limiter(s):
                yield self.Projection(s)


class FetchedImage:
    def __init__(self, name, processedData, rawData):
        self.Name = name
        self.ProcessedData = processedData
        self.RawData = rawData


def GetFetcher(config):
    if config.PickedFetcher == "rWallpapers":
        return rWallpapers()
    if config.PickedFetcher == "FromDirectory":
        return FromDirectory.FromPath(config.Fetcher.Path)

