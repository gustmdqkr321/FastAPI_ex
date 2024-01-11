import cv2
import numpy as np
import PIL
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

# YOLO 모델 로드
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")  # 가중치와 설정 파일
layer_names = net.getUnconnectedOutLayersNames()

# 이미지 읽기
image_path = '/Users/park_sh/Desktop/FastAPI_ex/desk2.jpeg'
image = cv2.imread(image_path)
height, width, _ = image.shape
# img_read = Image.open(image_path)
# img_arr = np.array(img_read)
# YOLO 입력 이미지로 변환
blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
# 이미지 크기 얻기
width, height,_ = image.shape
# YOLO 출력 얻기
outs = net.forward(layer_names)

# 검출된 객체의 정보 추출
class_ids = []
confidences = []
boxes = []

for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')
            x, y = int(center_x - w / 2), int(center_y - h / 2)
            boxes.append([x, y, int(w), int(h)])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Non-maximum suppression 수행
indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# 검출된 객체 그리기
for i in range(len(boxes)):
    if i in indices:
        x, y, w, h = boxes[i]
        label = str(class_ids[i])
        confidence = confidences[i]
        print(f"Object {i + 1} - Class ID: {label}, Confidence: {confidence:.2f}")
        print(f"    Bounding Box: (x: {x}, y: {y}, w: {w}, h: {h})")
        color = (0, 255, 0)
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        cv2.putText(image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# 결과 이미지 저장 또는 출력
# cv2.imwrite('output.jpg', image)
cv2.imshow("Object Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()