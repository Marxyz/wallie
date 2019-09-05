import subprocess
def SaveImage(image):
    path = os.
    return path

def SetWallpaper(path):
    filepath = f"file://{path}"
    cmd = f'gsettings set org.gnome.desktop.background picture-uri "{filepath}"'
    subprocess.run(cmd, shell=True)
    return path