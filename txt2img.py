import api_client
import gradio as gr

import torch
from PIL import Image
import numpy as np

model = torch.hub.load("yolov5", 'custom', "yolov5\yolov5s.pt", source='local')

def generate_image(prompt, negative_prompt, step_slider, width_slider, height_slider, model_dropdown, lora_dropdown):
    if lora_dropdown:
        prompt += ", " + lora_dropdown
    api_client.change_model(model_dropdown)
    result = api_client.api.txt2img(
        prompt=prompt, 
        negative_prompt=negative_prompt,
        seed=-1, 
        cfg_scale=7, 
        sampler_index="Euler a", 
        steps=step_slider, 
        width=width_slider, 
        height=height_slider, 
        save_images=True
    )
    # 실시간 미리보기
    # result2 = api_client.api.live_preview()

# Object Detection YOLOv5
    # Convert image to numpy array
    img_np = np.array(result.image)
    # Use YOLOv5 for object detection
    results = model(img_np)
    # Draw bounding boxes on the image
    results.render()
    # Convert image back to PIL format
    img_with_boxes = Image.fromarray(results.ims[0])

    # crops = results.crop(save=True)

    return result.image, img_with_boxes
    # return result.image

# def generate_image(prompt, negative_prompt, seed, cfg_scale, sampler_index, steps, height, width, save_images):
#     result = api_client.api.txt2img(
#         prompt=prompt,
#         negative_prompt=negative_prompt,
#         seed=seed, 
#         cfg_scale=cfg_scale, 
#         sampler_index=sampler_index, 
#         steps=steps, 
#         height=height, 
#         width=width, 
#         save_images=save_images
#     )
#     return result

# # images contains the returned images (PIL images)
# result1.images

# # image is shorthand for images[0]
# result1.image

# # info contains text info about the api call
# result1.info

# # info contains paramteres of the api call
# result1.parameters

# result1.image