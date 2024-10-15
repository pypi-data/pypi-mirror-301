
import os
import subprocess
import re
from pathlib import Path
import time
import cv2
from PIL import Image

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries","format=duration", "-of","default=noprint_wrappers=1:nokey=1", filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def get_hms(sec):
    hms = time.strftime('%H:%M:%S', time.gmtime(get_length(sec)))
    return hms

def frame(path, nskip):
    output = "./"+Path(path).stem+"-frame/"
    if os.path.exists(output) == False:
        os.mkdir(output)
    vidcap = cv2.VideoCapture(path)
    success,imgcv = vidcap.read()
    count = 0
    num = 0
    while success:
        if count%nskip == 0:
             cv2.imwrite(output+str(num)+".png", imgcv)
             num += 1
        success,imgcv = vidcap.read()
        count += 1
    print("extract frame finish")

def write(path, duration=15, resize=None, soundpath=None, output=None):
    path = path+"/"
    if output == None:
        output = Path(path).stem+"-video"
    if duration == 15 and soundpath != None:
        duration = get_length(soundpath)
    fps = len(os.listdir(path))/duration
    imgs = Image.open(path+"/"+os.listdir(path)[0])
    width, height = imgs.size
    cv2flag = cv2.INTER_NEAREST
    if resize != None:
        if resize[0] > width:
             cv2flag = cv2.INTER_CUBIC
        width, height = resize
    video = cv2.VideoWriter(output+".avi", cv2.VideoWriter_fourcc(*"XVID"), fps, (width, height))
    for i in range(0, len(os.listdir(path))):
        image = cv2.imread(path+"/"+str(i)+".png")
        if resize != None:
             image = cv2.resize(image, (width, height), interpolation = cv2flag)
        video.write(image)
    video.release()
    if soundpath == None:
        subprocess.run(["ffmpeg", "-i", output+".avi", "-c:v", "libx264", "-preset", "slow", "-crf", "23", output+".mp4"])
    else:
        subprocess.run(["ffmpeg", "-i", output+".avi", "-i", soundpath, "-c:v", "libx264", "-preset", "slow", "-crf", "23", output+".mp4"])
    if os.path.exists(output+".avi") == True:
        os.remove(output+".avi")
    print("save video finish")

def clip(path, start="00:00:00", end="00:00:00", crop=None, resize=None, output=None):
    if output == None:
        output = Path(path).stem+"-clip"
    vidcap = cv2.VideoCapture(path)
    totalframe = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    success,imgcv = vidcap.read()
    height, width, _ = imgcv.shape
    cv2flag = cv2.INTER_NEAREST
    if resize != None:
        if resize[0] > width:
             cv2flag = cv2.INTER_CUBIC
        width, height = resize
    duration = get_length(path)
    fps = totalframe/duration
    video = cv2.VideoWriter(output+".avi", cv2.VideoWriter_fourcc(*"XVID"), fps, (width, height))
    count = 0
    n = 0
    while success:
        n += duration/totalframe
        if type(crop) is tuple:
             imgcv = imgcv[crop[1][1]:crop[1][1]+crop[0][1], crop[1][0]:crop[1][0]+crop[0][0]]
        if type(crop) is list:
             for c in crop:
                  if get_hms(c["start"]) <= n and n <= get_hms(c["start"])+c["duration"]:
                       imgcv = imgcv[c["crop"][1][1]:c["crop"][1][1]+c["crop"][0][1], c["crop"][1][0]:c["crop"][1][0]+c["crop"][0][0]]
        imgcv = cv2.resize(imgcv, (width, height), interpolation = cv2flag)
        video.write(imgcv)
        success,imgcv = vidcap.read()
        count += 1
    video.release()
    if end == "00:00:00":
        end = time.strftime('%H:%M:%S', time.gmtime(get_length(path)))
    subprocess.run(["ffmpeg", "-ss", start, "-to", end, "-i", output+".avi", "-ss", start, "-to", end, "-i", path, "-map", "0:0", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "23", output+".mp4"])
    if os.path.exists(output+".avi") == True:
        os.remove(output+".avi")
    print("save video clip finish")
