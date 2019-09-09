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
        image = image.resize((150, 150))
        data = numpy.asarray(image)
        return FetchedImage(name, data)

    @classmethod
    def FromPath(cls, path):
        elements = [os.path.join(path,i) for i in os.listdir(path)]
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
    def __init__(self, name, imgData):
        self.Name = name
        self.Data = imgData


def GetFetcher(fetcherConf):
    if fetcherConf.PickedFetcher == "rWallpapers":
        return rWallpapers()
    if fetcherConf.PickedFetcher == "FromDirectory":
        return FromDirectory.FromPath(fetcherConf.Fetcher.Path)

