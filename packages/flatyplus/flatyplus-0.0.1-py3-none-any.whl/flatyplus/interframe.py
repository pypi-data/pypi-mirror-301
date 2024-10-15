
import os
import subprocess
import re
import cv2
from pathlib import Path


def interpolate(path, num=2):
    output = "./"+Path(path).stem+"-interframe/"
    output_temp = "./"+Path(path).stem+"-interframe-temp/"
    if os.path.exists(output) == False:
        os.mkdir(output)
    if os.path.exists(output_temp) == False:
        os.mkdir(output_temp)
    while(True):
        n = int((len(os.listdir(output)))/(2**num))
        if os.path.exists(path+str(n+1)+".png") == False:
             os.replace(path+str(n)+".png", output+str(len(os.listdir(output)))+".png")
             break
        subprocess.run(["interframe", "-i", path+str(n)+".png", path+str(n+1)+".png", "-o", output_temp, "-n", num])
        for f in os.listdir(output_temp):
             os.rename(output_temp+f, output_temp+re.sub("(.*)_", "", f))
        for f in range(0, (2**num)+1):
             if f != 2**num:
                  os.replace(output_temp+str(f)+".png", output+str(len(os.listdir(output)))+".png")
        print("\rextract interpolation: "+str(n), end=" ")
    subprocess.run(["rm", "-r", output_temp])
    print("save interpolation frame finish")
