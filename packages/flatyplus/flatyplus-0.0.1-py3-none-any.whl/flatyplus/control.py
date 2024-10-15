
import numpy as np
import cv2
import torch
import matplotlib
import matplotlib.cm
import numpy as np
from PIL import Image
from pathlib import Path
import os
from rembg import remove

torch.hub.help("intel-isl/MiDaS", "DPT_BEiT_L_384", force_reload=True)  # Triggers fresh download of MiDaS repo
model_zoe_n = torch.hub.load("isl-org/ZoeDepth", "ZoeD_NK", pretrained=True).eval()
model_zoe_n = model_zoe_n.to("cuda")


def colorize(value, vmin=None, vmax=None, cmap='gray_r', invalid_val=-99, invalid_mask=None, background_color=(128, 128, 128, 255), gamma_corrected=False, value_transform=None):
    if isinstance(value, torch.Tensor):
        value = value.detach().cpu().numpy()

    value = value.squeeze()
    if invalid_mask is None:
        invalid_mask = value == invalid_val
    mask = np.logical_not(invalid_mask)

    # normalize
    vmin = np.percentile(value[mask],2) if vmin is None else vmin
    vmax = np.percentile(value[mask],85) if vmax is None else vmax
    if vmin != vmax:
        value = (value - vmin) / (vmax - vmin)  # vmin..vmax
    else:
        # Avoid 0-division
        value = value * 0.

    # squeeze last dim if it exists
    # grey out the invalid values

    value[invalid_mask] = np.nan
    cmapper = matplotlib.cm.get_cmap(cmap)
    if value_transform:
        value = value_transform(value)
        # value = value / value.max()
    value = cmapper(value, bytes=True)  # (nxmx4)

    # img = value[:, :, :]
    img = value[...]
    img[invalid_mask] = background_color

    # gamma correction
    img = img / 255
    img = np.power(img, 2.2)
    img = img * 255
    img = img.astype(np.uint8)
    img = Image.fromarray(img)
    return img


def zoe_depth(image, resize):
    with torch.autocast("cuda", enabled=True):
        depth = model_zoe_n.infer_pil(image)
    depth = colorize(depth, cmap="gray_r")
    image = depth.resize(resize)
    return depth

def canny(image, resize):
    image = np.array(image)
    image = cv2.Canny(image, 100, 200)
    image = image[:, :, None]
    image = np.concatenate([image, image, image], axis=2)
    image = Image.fromarray(image)
    image = image.resize(resize)
    return image

def video(path, nskip, resize, output=None, rembg=False):
    if output == None:
        output = "./"+Path(path).stem+"-control"
    output = output+"/"
    if os.path.exists(output) == False:
        os.mkdir(output)
    if os.path.exists(output+"canny/") == False:
        os.mkdir(output+"canny/")
    if os.path.exists(output+"zoe_depth/") == False:
        os.mkdir(output+"zoe_depth/")
    vidcap = cv2.VideoCapture(path)
    success,imgcv = vidcap.read()
    totalframe = int((int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))/nskip)-1)
    count = 0
    num = 0
    while success:
        if count%nskip == 0:
              imgcv = cv2.cvtColor(imgcv, cv2.COLOR_BGR2RGB)
              imgcv = Image.fromarray(imgcv)
              zoe_depth(imgcv, resize).save(output+"zoe-depth/"+str(num)+".png")
              if rembg == True:
                   imgcv = remove(imgcv)
                   new_image = Image.new("RGBA", imgcv.size, "GREEN") # Create a white rgba background
                   new_image.paste(imgcv, (0, 0), imgcv)              # Paste the image on the background. Go to the links given below for details.
                   imgcv = new_image.convert('RGB')
              canny(imgcv, resize).save(output+"canny/"+str(num)+".png")
              num += 1
              print("\rextract control: "+str(num), end=" ")
        success,imgcv = vidcap.read()
        count += 1
    print("finish")

