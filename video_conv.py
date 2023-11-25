from moviepy.video.io.VideoFileClip import VideoFileClip
import os


def super_video_format(file_data, index="", start=0, end=0):
    file_path = temp(file_data, index)
    video_clip = VideoFileClip(file_path)
    duration = video_clip.duration
    if duration < 180:
        s = duration / 2 - 10
        e = s + 20
    else:
        s = start
        e = end
    return video_clip.subclip(s, e)


def temp(file_data, index=""):
    print('temp index -> ', index)
    file_temp_name = 'temp' + index + '.mp4'
    file_path = os.path.join('uploads', file_temp_name)
    file_data.save(file_path)
    return file_path
