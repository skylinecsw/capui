# import torch
# from PIL import Image

# # YOLOv5 모델 로드
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# # def background_remove(image):
# #     img = Image.open(image)
# #     results = model(img)
# #     results.render()  # bounding box 그리기
# #     for *box, conf, cls in results.xyxy[0]:  # 첫 번째 이미지의 모든 bbox
# #         x1, y1, x2, y2 = map(int, box)
# #         cropped_img = img.crop((x1, y1, x2, y2))
# #         return cropped_img  # 첫 번째 bbox에 대한 크롭된 이미지 반환

# def background_remover_and_bbox(image):
#     img = Image.open(image)
#     results = model(img)
#     results.render()  # bounding box 그리기
#     img_with_boxes = Image.fromarray(results.ims[0])  # bounding box가 그려진 이미지
#     for *box, conf, cls in results.xyxy[0]:  # 첫 번째 이미지의 모든 bbox
#         x1, y1, x2, y2 = map(int, box)
#         cropped_img = img.crop((x1, y1, x2, y2))
#         return img_with_boxes, cropped_img  # bounding box가 그려진 이미지와 첫 번째 bbox에 대한 크롭된 이미지 반환

########################################
######## rembg 라이브러리 쓴 코드 #######
########################################

# pip install rembg

import torch
from PIL import Image
from rembg import remove

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
        background_removed_img = remove(cropped_img)  # 크롭 이미지에서 배경제거
        return img_with_boxes, background_removed_img  #cropped_img  # bounding box가 그려진 이미지와 첫 번째 bbox에 대한 크롭된 이미지 반환

########################################################
######## rembg 라이브러리 쓴 코드 (파라미터값조절)########
########################################################
# import torch
# from PIL import Image
# from rembg import remove

# # YOLOv5 모델 로드
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# # def background_remove(image):
# #     img = Image.open(image)
# #     results = model(img)
# #     results.render()  # bounding box 그리기
# #     for *box, conf, cls in results.xyxy[0]:  # 첫 번째 이미지의 모든 bbox
# #         x1, y1, x2, y2 = map(int, box)
# #         cropped_img = img.crop((x1, y1, x2, y2))
# #         return cropped_img  # 첫 번째 bbox에 대한 크롭된 이미지 반환

# def background_remover_and_bbox(image):
#     img = Image.open(image)
#     results = model(img)
#     results.render()  # bounding box 그리기
#     img_with_boxes = Image.fromarray(results.ims[0])  # bounding box가 그려진 이미지
#     for *box, conf, cls in results.xyxy[0]:  # 첫 번째 이미지의 모든 bbox
#         x1, y1, x2, y2 = map(int, box)
#         cropped_img = img.crop((x1, y1, x2, y2))
#         parmas = {
#             "alpha_matting" : True,
#             "alpha_matting_foregorund_threshold" : 240,
#             "alpha_matting_background_threshold" : 15,
#             "alpha_matting_erode_structure_size" : 10,
#         }
#         background_removed_img = remove(cropped_img, **parmas)  # 크롭 이미지에서 배경제거

#         return img_with_boxes, background_removed_img  #cropped_img  # bounding box가 그려진 이미지와 첫 번째 bbox에 대한 크롭된 이미지 반환

