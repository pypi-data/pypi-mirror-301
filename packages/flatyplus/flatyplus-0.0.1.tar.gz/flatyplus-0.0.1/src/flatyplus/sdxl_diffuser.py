
import torch
import random
import os
from pathlib import Path
from diffusers.utils import load_image
from diffusers import StableDiffusionXLPipeline, ControlNetModel, StableDiffusionXLControlNetPipeline, AutoencoderKL, EulerAncestralDiscreteScheduler
import numpy as np

pipe = None
control = None

def init(model, control_mode=None):
    global control
    global pipe
    vae = AutoencoderKL.from_pretrained(
        "madebyollin/sdxl-vae-fp16-fix",
        torch_dtype=torch.float16,
        )
    if control_mode == None:
        control = none
        pipe = StableDiffusionXLPipeline.from_pretrained(
              model,
              custom_pipeline="lpw_stable_diffusion_xl",
              vae=vae,
              torch_dtype=torch.float16,
              use_safetensors=True,
              )
    else:
        control = control_mode
        controlnet=[]
        for c in control:
              controlnet.append(ControlNetModel.from_pretrained("diffusers/controlnet-"+c+"-sdxl-1.0",torch_dtype=torch.float16))
        pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
              model,
              controlnet=controlnet,
              vae=vae,
              torch_dtype=torch.float16,
              use_safetensors=True,
              )
    pipe.safety_checker = None
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
    pipe.to('cuda')

def lora(model, weight_name=None, fuse=False):
    global pipe
    if weight_name == None:
        pipe.load_lora_weights(model)
    else:
        pipe.load_lora_weights(model, weight_name=weight_name)
    if fuse == True:
        pipe.fuse_lora()

def image(prompt, size, control_img=None, negative_prompt="lowres, (bad), text, error, fewer, extra, missing, worst quality, jpeg artifacts, low quality, watermark, unfinished, displeasing, oldest, early, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract]", seed=None, guidance_scale=7, num_inference_steps=28, controlnet_conditioning_scale=None, output=None):
    if seed == None:
        seed = random.randint(0, 2147483647)
    generator = torch.Generator(device="cpu").manual_seed(seed)
    if control == None:
        img = pipe(
              prompt,
              negative_prompt=negative_prompt,
              width=size[0],
              height=size[1],
              guidance_scale=guidance_scale,
              num_inference_steps=num_inference_steps,
              generator=generator
              ).images[0]
    else:
        if controlnet_conditioning_scale == None:
              controlnet_conditioning_scale = []
              for c in control:
                    controlnet_conditioning_scale.append(0.5)
        img = pipe(
              prompt,
              image=control_img,
              negative_prompt=negative_prompt,
              width=size[0],
              height=size[1],
              guidance_scale=guidance_scale,
              controlnet_conditioning_scale=controlnet_conditioning_scale,
              num_inference_steps=num_inference_steps,
              generator=generator
              ).images[0]
    if output != None:
        img.save(output)
    print(seed)
    return img

def frame(prompt, size, path, negative_prompt="lowres, (bad), text, error, fewer, extra, missing, worst quality, jpeg artifacts, low quality, watermark, unfinished, displeasing, oldest, early, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract]", seed=None, guidance_scale=7, num_inference_steps=28, controlnet_conditioning_scale=None, output=None):
    if output == None:
        output = "./"+Path(path).stem+"-frame"
    output = output+"/"
    if os.path.exists(output) == False:
        os.mkdir(output)
    last = len(os.listdir(path+"/"+control[0]+"/"))
    num = 0
    while num<last:
        if os.path.exists(output+str(num)+".png") == False:
              control_img = []
              for c in control:
                    imgc = load_image(path+"/"+c+"/"+str(num)+".png")
                    control_img.append(imgc)
              image(prompt, size, control_img=control_img, negative_prompt=negative_prompt, seed=seed, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps, controlnet_conditioning_scale=controlnet_conditioning_scale, output=output+str(num)+".png")
        num += 1
        print("\rgenerate frame: "+str(num)+"/"+str(last), end=" ")
    print("finish")

def repairframe(prompt, size, path, repair, negative_prompt="lowres, (bad), text, error, fewer, extra, missing, worst quality, jpeg artifacts, low quality, watermark, unfinished, displeasing, oldest, early, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract]", seed=None, guidance_scale=7, num_inference_steps=28, controlnet_conditioning_scale=None, output=None):
    if output == None:
        output = "./"+Path(path).stem+"-frame"
    output = output+"/"
    if os.path.exists(output) == False:
        os.mkdir(output)
    for r in repair:
        control_img = []
        for c in control:
              imgc = load_image(path+"/"+c+"/"+str(r)+".png")
              control_img.append(imgc)
        image(prompt, size, control_img=control_img, negative_prompt=negative_prompt, seed=seed, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps, controlnet_conditioning_scale=controlnet_conditioning_scale, output=output+str(num)+".png")
        print("\rrepair frame: "+str(r), end=" ")
    print("finish")


