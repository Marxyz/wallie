import subprocess
import shutil
import os
import PIL.Image

def SaveImage(directory, name, data):
    if(not os.path.isdir(directory)):
        os.mkdir(directory)
    im = PIL.Image.fromarray(data)
    path = os.path.join(directory, name)
    im.save(path)
    return path

def SetWallpaper(path):
    filepath = f"file://{path}"
    cmd = f'gsettings set org.gnome.desktop.background picture-uri "{filepath}"'
    subprocess.run(cmd, shell=True)
    return path