import subprocess
import shutil

def SaveImage(path, image):
    with open(path, "wb") as file:
        image.raw.decode_content = True
        shutil.copyfileobj(image.raw, file)
    return path

def SetWallpaper(path):
    filepath = f"file://{path}"
    cmd = f'gsettings set org.gnome.desktop.background picture-uri "{filepath}"'
    subprocess.run(cmd, shell=True)
    return path