import os
import PIL.Image
import random
import numpy
import requests
import collections
import json
from io import BytesIO


RedditSubmission = collections.namedtuple(
    "RedditSubmission", "Title Url Score Width Height"
)
ResponseData = collections.namedtuple("ResponseData", "Response After")


class rWallpapers:
    baseUrl = "https://www.reddit.com/r/EarthPorn.json"

    def __init__(self):
        pass

    def Fetch(self):
        return self._CreateGen(self.Projection, self.Limiter)

    def Projection(self, redditSubmission):
        response = requests.get(redditSubmission.Url)
        name = (
            redditSubmission.Title.replace("/", "").replace(".", "").replace(" ", "-")
        )
        name = f"{name}.jpg"
        image = PIL.Image.open(BytesIO(response.content))
        res_image = image.resize((150, 150))
        rawdata = numpy.asarray(image)
        data = numpy.asarray(res_image)
        return FetchedImage(name, data, rawdata)

    def Limiter(self, redditSubmission):
        return (
            redditSubmission.Score > 1000
            and redditSubmission.Width >= 1500
            and redditSubmission.Height >= 1000
            and "external" not in redditSubmission.Url
        )

    def _CreateGen(self, projection, limiter):
        return ImageGen(self._CreateRedditWallpaperGen(), projection, limiter)

    def _CreateRedditWallpaperGen(self):
        after = None
        while True:
            print("Connecting")
            apiResponse = requests.get(
                self.baseUrl,
                params={"after": after},
                headers={"User-agent": "Wallie.py"},
            ).json()
            after = apiResponse["data"]["after"]
            submissions = apiResponse["data"]["children"]
            random.shuffle(submissions)
            for submission in submissions:
                yield RedditSubmission(
                    Title=submission["data"]["title"],
                    Url=submission["data"]["preview"]["images"][0]["source"][
                        "url"
                    ].replace("preview", "i"),
                    Score=submission["data"]["score"],
                    Width=submission["data"]["preview"]["images"][0]["source"]["width"],
                    Height=submission["data"]["preview"]["images"][0]["source"][
                        "height"
                    ],
                )


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
    def __init__(self, name, dataForRecognition, rawImage):
        self.Name = name
        self.ProcessedData = dataForRecognition
        self.RawData = rawImage


def GetFetcher(config):
    if config.PickedFetcher == "rWallpapers":
        return rWallpapers()
    if config.PickedFetcher == "FromDirectory":
        return FromDirectory.FromPath(config.Fetcher.Path)

