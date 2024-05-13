import gradio as gr
import txt2img
import img2img
import os

def open_folder(model_input_path):
    model_input_path = "stable-diffusion-webui\models\Stable-diffusion"
    try:
        os.system(f'explorer "{model_input_path}"')
        return
    except Exception as e:
        return f"오류가 발생했습니다: {e}"

open_model_folder = gr.Button(
    
)

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

#################### Txt2Img ####################

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

#################### Img2Img ####################

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

demo = gr.TabbedInterface(
    [txt2img_tab, img2img_tab], ["txt2img", "img2img"], 
    title="Asset Geneator",
    theme=theme
)

demo.launch()