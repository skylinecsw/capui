import requests
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from rembg import remove
import os
from datetime import datetime
import io

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model = AutoModelForCausalLM.from_pretrained("microsoft/Florence-2-large", torch_dtype=torch_dtype, trust_remote_code=True).to(device)
processor = AutoProcessor.from_pretrained("microsoft/Florence-2-large", trust_remote_code=True)

task_prompt = '<OD>'
bgremoved_images_directory = "background-removed-images"

def plot_bbox(image, data):
    # Create a figure and axes
    fig, ax = plt.subplots()

    # Display the image
    ax.imshow(image)

    # Plot each bounding box
    for bbox, label in zip(data['bboxes'], data['labels']):
        # Unpack the bounding box coordinates
        x1, y1, x2, y2 = bbox
        # Create a Rectangle patch
        rect = patches.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=1, edgecolor='r', facecolor='none')
        # Add the rectangle to the Axes
        ax.add_patch(rect)
        # Annotate the label
        plt.text(x1, y1, label, color='white', fontsize=8, bbox=dict(facecolor='red', alpha=0.5))

    # Remove the axis ticks and labels
    ax.axis('off')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Convert the BytesIO object to a PIL Image
    bbox_image = Image.open(buf)

    # Close the plot to free memory
    plt.close(fig)

    return bbox_image

def background_remover_and_bbox(image_path, padding=30):
    img = Image.open(image_path)

    base_name = os.path.basename(image_path)  # 이미지 원본 이름 추출
    name, ext = os.path.splitext(base_name)
    new_name = f"{name}_removed.png"

    current_date = datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join(bgremoved_images_directory, current_date)
    os.makedirs(folder_path, exist_ok=True)
    
    # 파일 이름 중복 확인 및 새로운 이름 생성
    image_save_path = os.path.join(folder_path, new_name)
    unique_suffix = 1
    while os.path.exists(image_save_path):  # 이미 존재하는 파일 이름인 경우
        new_name = f"{name}_removed_{unique_suffix}.png"
        image_save_path = os.path.join(folder_path, new_name)
        unique_suffix += 1

    # Run the model and process the image
    prompt = task_prompt
    inputs = processor(text=prompt, images=img, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}  # 입력 데이터 타입 변환
    inputs["input_ids"] = inputs["input_ids"].long()  # input_ids를 LongTensor로 변환
    generated_ids = model.generate(
      input_ids=inputs["input_ids"],
      pixel_values=inputs["pixel_values"].to(device, dtype=torch_dtype),
      max_new_tokens=1024,
      early_stopping=False,
      do_sample=False,
      num_beams=1,
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    parsed_answer = processor.post_process_generation(
        generated_text,
        task=task_prompt,
        image_size=(img.width, img.height)
    )

    img_with_boxes = plot_bbox(img, parsed_answer['<OD>'])  # bounding box가 그려진 이미지

    # 가장 큰 bbox 찾기
    max_area = 0
    largest_bbox = None
    for bbox in parsed_answer['<OD>']['bboxes']:
        x1, y1, x2, y2 = bbox
        area = (x2 - x1) * (y2 - y1)
        if area > max_area:
            max_area = area
            largest_bbox = bbox

    if largest_bbox:
        x1, y1, x2, y2 = largest_bbox
        # 여백을 추가하여 좌표 조정
        x1 = max(0, x1 - padding)
        y1 = max(0, y1 - padding)
        x2 = min(img.width, x2 + padding)
        y2 = min(img.height, y2 + padding)
        cropped_img = img.crop((x1, y1, x2, y2))
        background_removed_img = remove(cropped_img)  # 크롭 이미지에서 배경제거

        # 고유한 파일 이름 생성
        new_name = f"{name}_removed_largest.png"
        image_save_path = os.path.join(folder_path, new_name)
        unique_suffix = 1
        while os.path.exists(image_save_path):  # 이미 존재하는 파일 이름인 경우
            new_name = f"{name}_removed_largest_{unique_suffix}.png"
            image_save_path = os.path.join(folder_path, new_name)
            unique_suffix += 1

        background_removed_img.save(image_save_path)  # 이미지 저장

    return img_with_boxes, background_removed_img

    # for i, (bbox, label) in enumerate(zip(parsed_answer['<OD>']['bboxes'], parsed_answer['<OD>']['labels'])):  # 모든 bbox에 대해 반복
    #     x1, y1, x2, y2 = bbox
    #     # 여백을 추가하여 좌표 조정
    #     x1 = max(0, x1 - padding)
    #     y1 = max(0, y1 - padding)
    #     x2 = min(img.width, x2 + padding)
    #     y2 = min(img.height, y2 + padding)
    #     cropped_img = img.crop((x1, y1, x2, y2))
    #     background_removed_img = remove(cropped_img)  # 크롭 이미지에서 배경제거

    #     # 고유한 파일 이름 생성
    #     new_name = f"{name}_removed_{i}.png"
    #     image_save_path = os.path.join(folder_path, new_name)
    #     unique_suffix = 1
    #     while os.path.exists(image_save_path):  # 이미 존재하는 파일 이름인 경우
    #         new_name = f"{name}_removed_{i}_{unique_suffix}.png"
    #         image_save_path = os.path.join(folder_path, new_name)
    #         unique_suffix += 1

    #     background_removed_img.save(image_save_path)  # 이미지 저장

    # return img_with_boxes, background_removed_img