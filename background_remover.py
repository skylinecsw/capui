import torch
from PIL import Image

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# def background_remove(image):
#     img = Image.open(image)
#     results = model(img)
#     results.render()  # bounding box 그리기
#     for *box, conf, cls in results.xyxy[0]:  # 첫 번째 이미지의 모든 bbox
#         x1, y1, x2, y2 = map(int, box)
#         cropped_img = img.crop((x1, y1, x2, y2))
#         return cropped_img  # 첫 번째 bbox에 대한 크롭된 이미지 반환

def background_remover_and_bbox(image):
    img = Image.open(image)
    results = model(img)
    results.render()  # bounding box 그리기
    img_with_boxes = Image.fromarray(results.ims[0])  # bounding box가 그려진 이미지
    for *box, conf, cls in results.xyxy[0]:  # 첫 번째 이미지의 모든 bbox
        x1, y1, x2, y2 = map(int, box)
        cropped_img = img.crop((x1, y1, x2, y2))
        return img_with_boxes, cropped_img  # bounding box가 그려진 이미지와 첫 번째 bbox에 대한 크롭된 이미지 반환
