import gradio as gr
import txt2img
import img2img
import os
import img_viewer
import background_remover

def open_folder(model_input_path):
    model_input_path = "stable-diffusion-webui\models\Stable-diffusion"
    try:
        os.system(f'explorer "{model_input_path}"')
        return
    except Exception as e:
        return f"오류가 발생했습니다: {e}"

def get_model_names(folder_path, extensions):
    try:
        # 폴더 내의 모든 파일과 폴더를 리스트로 가져옵니다.
        all_files = os.listdir(folder_path)
        # 지정된 확장자를 가진 파일들을 필터링합니다.
        model_names = [file for file in all_files if file.endswith(extensions)]
        return model_names
    except Exception as e:
        return f"오류가 발생했습니다: {e}"

folder_path = "stable-diffusion-webui\models\Stable-diffusion"
extensions = (".ckpt", ".safetensors")

model_names = get_model_names(folder_path, extensions)

theme = gr.themes.Monochrome()

#################################################
#################### Txt2Img ####################
#################################################

with gr.Blocks() as text_to_img:
    prompt = gr.Textbox(
        label="Prompt",
        show_label=False,
        max_lines=2,
        placeholder="Enter positive prompt"
    )
    negative_prompt = gr.Textbox(
        label="Negative Prompt",
        show_label=False,
        max_lines=2,
        placeholder="Enter Negative prompt"
    )
    step_slider = gr.Slider(
        value=20,
        minimum=1,
        maximum=100,
        label="Step",
        show_label='True', 
        step=1
    )
    width_slider = gr.Slider(
        value=512,
        minimum=256,
        maximum=2048,
        label="Width",
        show_label='True', 
        step=64
    )
    height_slider = gr.Slider(
        value=512, 
        minimum=256, 
        maximum=2048, 
        label="Height", 
        show_label='True', 
        step=64
    )
    model_dropdown = gr.Dropdown(
        choices=model_names, 
        value='v1-5-pruned-emaonly.safetensors', 
        label="Select an Model"
    )
    button = gr.Button(
    value="Open Model Folder", 
    interactive=True, 
    )
    button.click(fn=open_folder)
    lora_list = [
        ('None', ''), 
        ('Texture', 'diffuse texture, <lora:DiffuseTexture_v11:1>'), 
        ('Metal Texture', 'metal texture, <lora:dirtymetal_textures_1:0.8>'), 
        ('Old school Texture', 'texture, old school, quake, <lora:Quake_Lora:1>'), 
        ('Book', 'book, <lora:FantasyIcons_Books_noFlip:1>'), 
        ('Gemstone', 'gemstone, <lora:FantasyIcons_Gemstones:1>'), 
        ('pixel sprites', 'pixel, pixel art, pixelart, xiangsu, xiang su, <lora:pixel sprites:1>'), 
        ('PixelAnimal', 'animal, pixel, pixel art, pixelart, xiangsu, xiang su, <lora:PixelAnimal:1>'), 
        ('Pixel Weapon(axe, sword, bow)', 'weapon, no humans, pixel, pixel art, pixelart, <lora:pixel sword:1>'), 
        ('Pixel Gun', 'gun, no humans, pixel, pixel art, pixelart, <lora:pixel gun:1>'), 
        ('Pixel Book', 'boox,pixel, pixel art, pixelart, xiangsu, xiang su, <lora:pixel book:1>'), 
        ('Pixel Bottle', 'bottle,pixel, pixel art, pixelart, xiangsu, xiang su, simple background, <lora:Pixel bottle:1>'), 
        ('Pixel Isometry', '((Isometry)), pixel, pixel art, solo, <lora:Pixel_Building2:1>'), 
    ]
    lora_dropdown = gr.Dropdown(
        choices=lora_list,
        value='', 
        label="Select an LoRA",
    )
    t2i_result = gr.Image(

    )
    txt2img_tab = gr.Interface(
        fn = txt2img.generate_image,
        inputs=[prompt,negative_prompt,step_slider,width_slider,height_slider,model_dropdown,lora_dropdown], 
        outputs=[t2i_result],
        allow_flagging='never', 
        # outputs=["image", "image"],
    )
#################################################
#################### Img2Img ####################
#################################################

with gr.Blocks() as img_to_img:
    i2i_input = gr.Image(
        show_label=False,
    )

    i2i_prompt = gr.Textbox(
        label="Prompt",
        show_label=False,
        max_lines=2,
        placeholder="Enter positive prompt"
    )
    i2i_negative_prompt = gr.Textbox(
        label="Negative Prompt",
        show_label=False,
        max_lines=2,
        placeholder="Enter Negative prompt"
    )
    i2i_step_slider = gr.Slider(
        value=20,
        minimum=1,
        maximum=100,
        label="Step",
        show_label='True', 
        step=1
    )
    i2i_width_slider = gr.Slider(
        value=512,
        minimum=256,
        maximum=2048,
        label="Width",
        show_label='True', 
        step=64
    )
    i2i_height_slider = gr.Slider(
        value=512,
        minimum=256,
        maximum=2048,
        label="Height",
        show_label='True', 
        step=64
    )
    i2i_model_dropdown = gr.Dropdown(
        choices=model_names,
        value='v1-5-pruned-emaonly.safetensors', 
        label="Select an Model"
    )
    i2i_lora_list = [
        ('None', ''), 
        ('Texture', 'diffuse texture, <lora:DiffuseTexture_v11:1>'), 
        ('Metal Texture', 'metal texture, <lora:dirtymetal_textures_1:0.8>'), 
        ('Old school Texture', 'texture, old school, quake, <lora:Quake_Lora:1>'), 
        ('Book', 'book, <lora:FantasyIcons_Books_noFlip:1>'), 
        ('Gemstone', 'gemstone, <lora:FantasyIcons_Gemstones:1>'), 
        ('pixel sprites', 'pixel, pixel art, pixelart, xiangsu, xiang su, <lora:pixel sprites:1>'), 
        ('PixelAnimal', 'animal, pixel, pixel art, pixelart, xiangsu, xiang su, <lora:PixelAnimal:1>'), 
        ('Pixel Weapon(axe, sword, bow)', 'weapon, no humans, pixel, pixel art, pixelart, <lora:pixel sword:1>'), 
        ('Pixel Gun', 'gun, no humans, pixel, pixel art, pixelart, <lora:pixel gun:1>'), 
        ('Pixel Book', 'boox,pixel, pixel art, pixelart, xiangsu, xiang su, <lora:pixel book:1>'), 
        ('Pixel Bottle', 'bottle,pixel, pixel art, pixelart, xiangsu, xiang su, simple background, <lora:Pixel bottle:1>'), 
        ('Pixel Isometry', '((Isometry)), pixel, pixel art, solo, <lora:Pixel_Building2:1>'), 
    ]
    i2i_lora_dropdown = gr.Dropdown(
        choices=lora_list,
        value='', 
        label="Select an LoRA",
    )
    denoising_strength_silder = gr.Slider(
        value=0.5,
        minimum=0,
        maximum=1,
        label="Denoising Strength",
        show_label='True', 
        step=0.05
    )
    i2i_result = gr.Image(

    )

    img2img_tab = gr.Interface(
        fn = img2img.generate_img2img,
        inputs=[i2i_input,i2i_prompt,i2i_negative_prompt,i2i_step_slider,i2i_width_slider,i2i_height_slider,denoising_strength_silder,i2i_model_dropdown,i2i_lora_dropdown],
        outputs=[i2i_result],
        allow_flagging='never', 
    )

img_viewer_tab = gr.Interface(
    fn=img_viewer.load_images_from_folder,
    inputs=gr.Dropdown(label="Folder Path", choices=img_viewer.get_folders_in_directory("stable-diffusion-webui/output/txt2img-images")),
    outputs=gr.Gallery(label="Images"),
    title="Image Viewer",
    description="Load and display images from a folder.", 
    allow_flagging='never', 
)

# Background Remover 탭 추가
# background_remover_tab = gr.Interface(
#     fn=background_remover.background_remove,
#     inputs=gr.Image(type="filepath", label="Upload Image"),
#     outputs=gr.Image(label="Cropped Image"),
#     title="Background Remover",
#     description="Remove background using YOLOv5.", 
#     allow_flagging='never', 
# )
background_remover_tab = gr.Interface(
    fn=background_remover.background_remover_and_bbox,
    inputs=gr.Image(type="filepath", label="Upload Image"),
    outputs=[gr.Image(label="Image with Bounding Boxes"), gr.Image(label="Cropped Image")],
    title="Background Remover",
    description="Detect objects and remove background using YOLOv5."
)

demo = gr.TabbedInterface(
    [text_to_img, img_to_img, img_viewer_tab, background_remover_tab], ["txt2img", "img2img", "Image Viewer", "Background Remover"], 
    title="Asset Geneator",
    theme=theme
)

demo.launch()

#################################################
#################### Inpaint ####################
#################################################
        
# with gr.Blocks() as inpaint_image:
#     with gr.Row():
#         with gr.Column():
#             in_input = gr.Image(show_label=False)
#             in_mask = gr.ImageMask(show_label=False)
#             in_prompt = gr.Textbox(
#                 label="Prompt",
#                 show_label=True,
#                 max_lines=2,
#                 placeholder="Enter positive prompt", 
#             )
#             in_negative_prompt = gr.Textbox(
#                 label="Negative Prompt",
#                 show_label=True,
#                 max_lines=2,
#                 placeholder="Enter Negative prompt", 
#             )
#             in_step_slider = gr.Slider(
#                 value=20,
#                 minimum=1,
#                 maximum=100,
#                 label="Step",
#                 show_label=True, 
#                 step=1
#             )
#             in_width_slider = gr.Slider(
#                 value=512,
#                 minimum=256,
#                 maximum=2048,
#                 label="Width",
#                 show_label=True, 
#                 step=64
#             )
#             in_height_slider = gr.Slider(
#                 value=512,
#                 minimum=256,
#                 maximum=2048,
#                 label="Height",
#                 show_label=True, 
#                 step=64
#             )
#             denoising_strength_silder = gr.Slider(
#                 value=0.6,
#                 minimum=0,
#                 maximum=1,
#                 label="Denoising Strength",
#                 show_label=True, 
#                 step=0.05
#             )
#             with gr.Row():
#                 in_model_dropdown = gr.Dropdown(
#                     choices=model_names,
#                     value='v1-5-pruned-emaonly.safetensors', 
#                     label="Select an Model", 
#                     show_label=True, 
#                     scale=4, 
#                 )
#                 model_open_button = gr.Button(
#                     value="Open Model Folder", 
#                     interactive=True, 
#                     scale=1, 
#                 )
#                 model_open_button.click(fn=open_folder, inputs=[], outputs=[])
#             in_lora_dropdown = gr.Dropdown(
#                 choices=lora_list,
#                 value='', 
#                 label="Select an LoRA",
#                 show_label=True, 
#             )

#         with gr.Column():
#             generate_button = gr.Button("Generate Image")
#             i2i_result = gr.Image()

#         generate_button.click(
#             fn=inpaint.generate_inpaint,
#             inputs=[in_input, in_prompt, in_negative_prompt, in_step_slider, in_width_slider, in_height_slider, denoising_strength_silder, in_model_dropdown, in_lora_dropdown],
#             outputs=i2i_result
#             )




# txt2img.py
# in def generate_image

# # Object Detection YOLOv5
#     # Convert image to numpy array
#     img_np = np.array(result.image)
#     # Use YOLOv5 for object detection
#     results = model(img_np)
#     # Draw bounding boxes on the image
#     results.render()
#     # Convert image back to PIL format
#     img_with_boxes = Image.fromarray(results.ims[0])

#     # # Load the original image
#     # image = result.image
#     # img = cv2.imread(image)

#     # # Extract bounding boxes
#     # boxes = results[0].boxes.xyxy.tolist()

#     # # Iterate through the bounding boxes
#     # for i, box in enumerate(boxes):
#     #     x1, y1, x2, y2 = box
#     #     # Crop the object using the bounding box coordinates
#     #     ultralytics_crop_object = img[int(y1):int(y2), int(x1):int(x2)]
#     #     # Save the cropped object as an image
#     #     cv2.imwrite('ultralytics_crop_' + str(i) + '.png', ultralytics_crop_object)

#     # crops = results.crop(save=True)

#     # return result.image, img_with_boxes