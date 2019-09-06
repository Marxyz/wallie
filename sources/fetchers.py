import os
import PIL
import random
import numpy

class rWallpapers:
    def __init__(self):
        pass

    def Fetch(self):
        pass


class FromDirectory:    
    def __init__(self, dirEnumerate):
        self.DirContents = random.shuffle(dirEnumerate)
        self.limiter = lambda i: True


    def Fetch(self):
        
        return self._CreateGen(self.DirContents, self.Projection, self.limiter)

    def _CrateGen(self, elements, projectionFunc, limiter):
        return ImageGen(source, projectionFunc, limiter)

    def Projection(self, imagePath):
        name = os.path.split(imagePath)[1]
        data = numpy.asarray(PIL.Image.open(imagePath))
        return FetchedImage(name, data)

    @classmethod
    def FromPath(cls, path):
        elements = os.listdir(path)
        return FromDirectory(elements)

class ImageGen:
    def __init__(self,source, projection, limiter):
        self.Source = source
        self.Projection = projection
        self.Limiter = limiter

    
    def __iter__(self):
        for s in source:
            if(self.limiter(s)):
                yield self.projection(s)




class FetchedImage:
    def __init__(self, name, imgData):
        self.Name = name
        self.Data = imgData

def GetFetcher(fetcherConf):
    if fetcherConf.Name == "rWallpapers":
        return rWallpapers()
    if fetcherConf.Name == "FromDirectory":
        return FromDirectory.FromPath(fetcherConf.Path)

