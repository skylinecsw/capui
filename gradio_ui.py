import gradio as gr
import txt2img

theme = gr.themes.Monochrome()

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

model_list = [
    ('v1-5-pruned-emaonly', 'v1-5-pruned-emaonly.safetensors'), 
    ('pixelsprite, 16bitscene', 'allInOnePixelModel_v1.ckpt'), 
    ('anime', 'animesfw-latest.ckpt'), 
    ('AnyLora', 'anyloraCheckpoint_bakedvaeBlessedFp16.safetensors'), 
]
# model_list = [api_client.get_model_list()]
# print(model_list)
model_dropdown = gr.Dropdown(
    choices=model_list,
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

iface = gr.Interface(
    fn = txt2img.generate_image,
    inputs=[prompt,negative_prompt,step_slider,width_slider,height_slider,model_dropdown,lora_dropdown],
    outputs=["image", "image"],
    title="Asset Geneator",
    allow_flagging='never', 
    theme=theme
)

iface.launch()