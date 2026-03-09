import subprocess
import os, tempfile
import zipfile
from lib import msg
import cv2
import numpy as np

def f1_download_video_from_url(params:dict):
    result = None
    try:
        if params.keys() == msg.f1_download_video_from_url_params.keys():
            target_folder = params.get("targetFolder", "")
            file_name = params.get("fileName", "")
            file_extension = params.get("fileExtension", "mp4")
            url = params.get("url", "")
            # Ensure folder exists
            os.makedirs(target_folder, exist_ok=True)
            output_path = os.path.join(
                target_folder,
                f"{file_name}.{file_extension}"
            )
            result = subprocess.run([
                "/usr/local/bin/yt-dlp",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "-o", output_path,
                url
            ], capture_output=True, check=True)
            print("STDOUT:\n", result.stdout)
            print("STDERR:\n", result.stderr)
            print("Return code:", result.returncode)
        else:
            print(f" wrong parameter set {params}, must be {msg.f1_download_video_from_url_params}")
    except Exception as e:
        print(f" [download_video_from_url] exception :: {e}")

def f2_download_audio_from_url(params:dict):
    try:
        if params.keys() == msg.f2_download_audio_from_url_params.keys():
            subprocess.run([
                "yt-dlp",
                "best-audio",
                "--audio-format", "mp3",
                "--audio-quality", "192K",
                "-o", f"{params.get("targetFolder","")}//{params.get("fileName","")}.{params.get("fileExtension","mp3")}",
                f"{params.get("url","")}"
            ], capture_output=True)
        else:
            print(f" wrong parameter set {params}, must be {msg.f2_download_audio_from_url_params}")
    except Exception as e:
        print(f" [download_video_from_url] exception :: {e}")

def f3_split_local_video_in_frames(params: dict):
    try:
        video_path = params.get("localVideoPath")
        zip_target_path = params.get("zipTargetPath")
        frame_differential_threshold = params.get("frameDifferentialThreshold", 50)
        target_fps = params.get("fps", 5)
        if not video_path or not zip_target_path:
            raise ValueError("Missing required parameters")
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")
        cap = cv2.VideoCapture(video_path)
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = max(int(original_fps / target_fps), 1)
        with tempfile.TemporaryDirectory() as temp_dir:
            frame_index = 0
            saved_index = 0
            cumulo = 0
            last_saved_small = None
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_index % frame_interval != 0:
                    frame_index += 1
                    continue
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray_small = cv2.resize(gray, (64, 64), interpolation=cv2.INTER_AREA)
                save_frame = False
                if last_saved_small is None:
                    save_frame = True
                else:
                    diff = np.mean(cv2.absdiff(gray_small, last_saved_small))
                    cumulo = cumulo + diff
                    if diff > frame_differential_threshold:
                        save_frame = True
                if save_frame:
                    file_name = f"frame_{saved_index:06d}.jpg"
                    full_path = os.path.join(temp_dir, file_name)
                    cv2.imwrite(full_path, frame)
                    last_saved_small = gray_small
                    saved_index += 1
                frame_index += 1
            cap.release()
            print(f"\n----------- INPUT -------------")
            print(f"fps ::{target_fps}")
            print(f"threshold ::{frame_differential_threshold}")
            print(f"------------- RESULT ------------")
            print(f"avg differenza ::{cumulo/frame_index}")
            print(f"frame analizzati::{frame_index}")
            print(f"frame salvati::{saved_index}")
            print(f"ratio salvati::{saved_index/frame_index}")
            print(f"-----------------------------------\n")
            os.makedirs(os.path.dirname(zip_target_path), exist_ok=True)
            with zipfile.ZipFile(zip_target_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file_name in sorted(os.listdir(temp_dir)):
                    full_path = os.path.join(temp_dir, file_name)
                    zipf.write(full_path, arcname=file_name)
        print(f"Frames successfully saved to: {zip_target_path}")
    except Exception as e:
        print(f"[f3_split_local_video_in_frames] exception :: {e}")