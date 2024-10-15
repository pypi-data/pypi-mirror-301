
import os
import subprocess
import cv2
from yt_dlp import YoutubeDL

def getTitle(url):
    with YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        return video_title

def audio(url, clip=None, output=None):
    if output == None:
        output = getTitle(url)
    subprocess.run(["yt-dlp", "-o", output+"-temp.m4a", "-f", "ba", "-S", "aext:m4a", url])
    if clip == None:
        os.rename(output+"-temp.m4a", output+".m4a")
    else:
        subprocess.run(["ffmpeg", "-ss", clip[0], "-to", clip[1], "-i", output+"-temp.m4a", "-c", "copy", output+".m4a"])
    if os.path.exists(output+"-temp.m4a") == True:
        os.remove(output+"-temp.m4a")
    print("save audio")

def video(url, short=False, clip=None, output=None):
    if output == None:
        output = getTitle(url)
    if short == True:
        subprocess.run(["yt-dlp", "-o", output+"-temp.mp4", "-f", "bv", "-S", "width:1280,vext:mp4", url])
    else:
        subprocess.run(["yt-dlp", "-o", output+"-temp.mp4", "-f", "bv", "-S", "height:1280,vext:mp4", url])
    if clip == None:
        os.rename(output+"-temp.mp4", output+".mp4")
    else:
        subprocess.run(["ffmpeg", "-ss", clip[0], "-to", clip[1], "-i", output+"-temp.mp4", "-c", "copy", output+".mp4"])
    print("save video")

def audiovideo(url, short=False, clip=None, output=None):
    if output == None:
        output = getTitle(url)
    audio(url, clip, output)
    video(url, short, clip, output)
    os.rename(output+".m4a", output+"-temp.m4a")
    os.rename(output+".mp4", output+"-temp.mp4")
    subprocess.run(["ffmpeg", "-i", output+"-temp.mp4", "-i", output+"-temp.m4a", "-c:v", "libx264", "-preset", "slow", "-crf", "23", output+".mp4"])
    if os.path.exists(output+"-temp.m4a") == True:
        os.remove(output+"-temp.m4a")
    if os.path.exists(output+"-temp.mp4") == True:
        os.remove(output+"-temp.mp4")
    print("save audiovideo")

