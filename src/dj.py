import traceback
import subprocess

lines = []

##### scarica le canzoni #############

try:
    # read requirements file
    with open('lista.txt') as f:
        lines = f.readlines()
except:
    traceback.print_exc()

for url in lines:
    try:
        subprocess.run(["/home/gio81/.local/bin/yt-dlp", "best-audio", "--extract-audio", "--audio-format","mp3", "--audio-quality","192K", url], capture_output=True)
        print("lanciato "+url)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")

print("canzoni: finito")

##### scarica i video #############

try:
    # read requirements file
    with open('film.txt') as f:
        lines = f.readlines()
except:
    traceback.print_exc()

for url in lines:
    try:
        subprocess.run(["/home/gio81/.local/bin/yt-dlp", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", url], capture_output=True)
        print("lanciato "+url)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")

print("film: finito")
