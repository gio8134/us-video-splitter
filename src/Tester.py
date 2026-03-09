from lib import lib

f1_download_video_from_url_params_test = {
    "url":"https://hello.porn/get_file/13/78df6907790f55438e9779fef6d007b9/711000/711374/711374_720p.mp4/",
    "targetFolder":"/home/gio81/temp/",
    "fileName":"madisonivyyoung",
    "fileExtension":"mp4"
}

f3_split_local_video_in_frames_params_test = {
    "localVideoPath":"/home/gio81/temp/madisonivyyoung.mp4",
    "zipTargetPath":"/home/gio81/temp/madisonivyyoung.zip",
    "frameDifferentialThreshold":21,
    "fps":21
}

print("step 1 - download the file ")
lib.f1_download_video_from_url(f1_download_video_from_url_params_test)

print("step 2 - zip the frames ")
lib.f3_split_local_video_in_frames(f3_split_local_video_in_frames_params_test)
