import cv2
import gradio as gr
import requests
import numpy as np
from PIL import Image
from requests.auth import HTTPBasicAuth
import logging


def set_boxes(data, image_bgr):
    # 박스 색상
    colors = {
        "RASPBERRY PICO": (0, 255, 0),  # 초록색
        "USB": (255, 0, 0),  # 파란색
        "BOOTSEL": (0, 0, 255),  # 빨간색
        "OSCILLATOR": (255, 255, 0),  # 하늘색
        "CHIPSET": (255, 0, 255),  # 분홍색
        "HOLE": (0, 255, 255),  # 노란색
    }

    objects = data.get('objects', [])
    if not objects:
        logging.warning("Superb AI에서 Model 키세요!!!")
        return

    for obj in objects:
        class_name = obj['class']
        score = obj['score']
        box = obj['box']  # [x1, y1, x2, y2]

        start_point = (box[0], box[1])  # 좌측 상단 (x1, y1)
        end_point = (box[2], box[3])  # 우측 하단 (x2, y2)

        cv2.rectangle(image_bgr, start_point, end_point, colors.get(class_name, (255, 255, 255)), 2)

        label = f"{class_name} ({score:.2f})"
        label_position = (box[0], box[1] - 10)
        cv2.putText(image_bgr, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    colors.get(class_name, (255, 255, 255)), 1)


def process_image(image, VISION_API_URL, TEAM, ACCESS_KEY):
    image = np.array(image)
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    _, img_encoded = cv2.imencode(".jpg", image_bgr)

    try:
        response = requests.post(
            VISION_API_URL,
            auth=HTTPBasicAuth(TEAM, ACCESS_KEY),
            headers={"Content-Type": "image/jpeg"},
            data=img_encoded.tobytes(),
        )
        response_data = response.json()
        print(response_data)

        set_boxes(response_data, image_bgr)

    except Exception as e:
        print(f"Error during API call: {e}")

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(image_rgb)


def start_gradio(VISION_API_URL, TEAM, ACCESS_KEY):
    iface = gr.Interface(
        fn=lambda img: process_image(img, VISION_API_URL, TEAM, ACCESS_KEY),
        inputs=gr.Image(type="pil"),
        outputs="image",
        title="Vision AI Object Detection",
        description="Upload an image to detect objects using Vision AI.",
    )
    iface.launch(share=True)