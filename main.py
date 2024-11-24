from Network.ApiService import ApiService
from requests.auth import HTTPBasicAuth
import serial
# from Tools.DataAugment import set_data_augment
# from Tools.Gradio import start_gradio
# from Tools.CheckImage import show_imaged
import time
import Inference_Pico
import requests
import os
import time
import confusion_matrix
import check_objects
from io import BytesIO
import cv2

ser = serial.Serial("/dev/ttyACM0", 9600)

def crop_img(img, size_dict):
    x = size_dict["x"]
    y = size_dict["y"]
    w = size_dict["width"]
    h = size_dict["height"]
    img = img[y : y + h, x : x + w]
    return img

def use_cloud_server(img):
    URL = "https://suite-endpoint-api-apne2.superb-ai.com/endpoints/be320cd2-d2bd-4e17-bc9a-4398e26d1f23/inference"
    ACCESS_KEY = "fFJOF6bXM75WTU3qTKADi2DfJRVpcJXk5vAdEep2"

    # with open(img, "rb") as image_file:
    #     image_data = image_file.read()

    _, img_encoded = cv2.imencode(".jpg", img)

    # Prepare the image for sending
    img_bytes = BytesIO(img_encoded.tobytes())

    # Send the image to the API
    image_data = {"file": ("image.jpg", img_bytes, "image/jpeg")}

    try:
        response = requests.post(
            url=URL,
            auth=HTTPBasicAuth("kdt2024_1-9", ACCESS_KEY),
            headers={"Content-Type": "image/jpeg"},
            data=image_data,
        )
        return response.json()
    except requests.RequestException as e:
        print(f"Error uploading {img}: {e}")


def get_img():
    cam = cv2.VideoCapture(2)

    if not cam.isOpened():
        print("Camera Error")
        exit(-1)

    ret, img = cam.read()
    cam.release()

    if not ret:
        print("Failed to capture image")
        exit(-1)

    return img

def check_pico():
    # data = test_image_detection()
    while True:
        data = ser.read()
        print(f"Data received from serial: {data}")

        if data == b"0":
            img = get_img()

            # Crop information (set to None if no cropping is needed)
            crop_info = {"x": 20, "y": 100, "width": 600, "height": 600}

            if crop_info is not None:
                img = crop_img(img, crop_info)

            # test 이미지
            # img = "/Users/jeonsangmin/Desktop/test_img_/test_img_82.jpg"

            data = use_cloud_server(img)
            Inference_Pico.show_image(img, data)
            centers, objects_data, is_flag = confusion_matrix.process_images(data, "test_img_80.jpg")
            print(centers, objects_data, is_flag)

            if not is_flag:
                print("9개 다 안잡힘")
                return

            is_fair_quality = check_objects.validate_positions(centers, objects_data)
            print(f"품질 결과: {is_fair_quality}")

            if not is_fair_quality:
                print("불량 입니다.")

            if is_fair_quality:
                ser.write(b"0")
                # print("불량")
                time.sleep(3)  # 3초 대기
                ser.write(b"1")
                # print("재가동")
            else:
                ser.write(b"1")
                # print("정상")

        else:
            ser.write(b"0")
            print("Response sent to serial: 0")

        time.sleep(0.05)


if __name__ == "__main__":
    # Test both endpoints
    # print("Testing server start...")
    # test_start_server()

    # time.sleep(1)
    # print("\nTesting image detection...")

    # Pico 검출
    _ = check_pico()

    # False일 때 컨베이어 멈추기






