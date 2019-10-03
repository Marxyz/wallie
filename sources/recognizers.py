import warnings
import collections

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)

    import numpy
    import os
    import sys
    import PIL.Image

    stderr = sys.stderr
    sys.stderr = open("/dev/null", "w")
    import keras

    sys.stderr = stderr

    import tensorflow as tf
    import logging

    logger = tf.get_logger()
    logger.setLevel(logging.ERROR)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.getLogger("tensorflow").setLevel(logging.FATAL)


Label = collections.namedtuple("Label", "Confidence Description")


class IntelImagesRecognizer:

    Classes = {
        "Buildings": 0,
        "Forest": 1,
        "Glacier": 2,
        "Mountain": 3,
        "Sea": 4,
        "Street": 5,
    }

    @classmethod
    def FromPath(cls, path):
        model = keras.models.load_model(path)
        return IntelImagesRecognizer(model)

    def __init__(self, model):
        self.LoadedModel = model

    def Recognize(self, image):
        img_tensor = self._LoadImage(image)
        inv_classes = {int(v): k for k, v in self.Classes.items()}
        predictions = self.LoadedModel.predict(img_tensor)[0]
        res = {}
        for ind, p in enumerate(predictions):
            res[inv_classes[ind]] = numpy.around(p, 3)
        m = max(res, key=lambda key: res[key])

        return Label(Confidence=res[m], Description=m)

    def _LoadImage(self, image):

        if type(image) == str:
            img = keras.preprocessing.image.load_img(image, target_size=(150, 150))
        else:
            img = image
        img_tensor = keras.preprocessing.image.img_to_array(img)
        img_tensor = numpy.expand_dims(img_tensor, axis=0)
        img_tensor /= 255.0
        return img_tensor


def GetRecognizer(config):
    if config.PickedRecognizer != "None":
        if config.PickedRecognizer == "IntelNature":
            return IntelImagesRecognizer.FromPath(config.Recognizer.Path)

