import subprocess
import shutil
import os
import PIL.Image

def SaveImage(path, image):
    d = os.path.split(path)[0]
    if(not os.path.isdir(d)):
        os.mkdir(d)
    im = PIL.Image.fromarray(image)
    im.save(path)
    return path

def SetWallpaper(path):
    filepath = f"file://{path}"
    cmd = f'gsettings set org.gnome.desktop.background picture-uri "{filepath}"'
    subprocess.run(cmd, shell=True)
    return path