import gradio as gr
from txt2img import generate_image

prompt = gr.Text(
    label="Prompt",
    show_label=False,
    max_lines=2,
    placeholder="Enter positive prompt",
    container=False,
)
negative_prompt = gr.Text(
    label="Negative Prompt",
    show_label=False,
    max_lines=2,
    placeholder="Enter Negative prompt",
    container=False,
)
width_slider = gr.Slider(
    value=512,
    minimum=256,
    maximum=2048,
    label="Width",
    show_label="True",
    step=64,
    container=False,
)
height_slider = gr.Slider(
    value=512,
    minimum=256,
    maximum=2048,
    label="Height",
    show_label="True",
    step=64,
    container=False,
)

lora_list = ["Dog", "Cat", "Bird", "Fish"]
lora_dropdown = gr.Dropdown(
    choices=lora_list,
    label="Select an LoRA",
    value=None
)

iface = gr.Interface(
    fn = generate_image,
    inputs=[prompt,negative_prompt,width_slider,height_slider,lora_dropdown],
    outputs="image",
    title="Text to Image Generation",
    allow_flagging=False
)

iface.launch()