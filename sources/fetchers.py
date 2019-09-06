class rWallpapers:

    def __init__(self):
        pass

    
    def Fetch(self):
        pass


class FromDirectory:

    def __init__(self):
        pass


def GetFetcher(name):
    if name == "rWallpapers":
        return rWallpapers()
    if name == "FromDirectory":
        return FromDirectory()
        

    