import gradio as gr
import txt2img

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
    ('pixelsprite, 16butscene', 'allInOnePixelModel_v1.ckpt'), 
    ('anime style', 'animesfw-latest.ckpt'), 
]
model_dropdown = gr.Dropdown(
    choices=model_list,
    value='', 
    label="Select an Model",
)
lora_list = [
    ('None', ''), 
    ('Texture', 'diffuse texture, <lora:DiffuseTexture_v11:1>'), 
    ('Metal Texture', 'metal texture, <lora:dirtymetal_textures_1:0.8>'), 
    ('Old school Texture', 'texture, old school, quake, <lora:Quake_Lora:1>'), 
    ('Book', 'book, <lora:FantasyIcons_Books_noFlip:1>'), 
    ('Gemstone', 'gemstone, <lora:FantasyIcons_Gemstones:1>')
]
lora_dropdown = gr.Dropdown(
    choices=lora_list,
    value='', 
    label="Select an LoRA",
)

iface = gr.Interface(
    fn = txt2img.generate_image,
    inputs=[prompt,negative_prompt,width_slider,height_slider,model_dropdown,lora_dropdown],
    outputs="image",
    title="Asset Generator",
    allow_flagging='never'
)

iface.launch()