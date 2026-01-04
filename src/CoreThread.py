import threading
import time
import cv2
import os
from Env import Env


class CoreThread(threading.Thread):
    
    def __init__(self, name, origin_video_name):
        super().__init__()
        self.name = name
        self.env = Env().get_env()
        self.video_origin_path = self.env['ORIDIR'] + origin_video_name
        self.img_dest_folder = self.env['DESTDIR'] 

    def run(self):
        print(f"[CoreThread]::{self.name} started")
        cap = cv2.VideoCapture(self.video_origin_path)
        if not cap.isOpened():
            raise IOError(f"[CoreThread]::{self.name} ::: CANNOT OPEN VIDEO FILE")
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_filename = os.path.join(
                self.img_dest_folder, f"frame_{frame_count:06d}.jpg"
            )
            cv2.imwrite(frame_filename, frame)
            frame_count += 1
        cap.release()
        print(f"Extracted {frame_count} frames")