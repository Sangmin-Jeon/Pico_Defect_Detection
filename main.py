import requests
import cv2
from requests.auth import HTTPBasicAuth
import time
import Inference_Pico
import confusion_matrix
import check_objects
import lenght
from io import BytesIO

def crop_img(img, size_dict):
    """ Crop the image based on the provided bounding box. """
    x = size_dict["x"]
    y = size_dict["y"]
    w = size_dict["width"]
    h = size_dict["height"]
    return img[y:y+h, x:x+w]

def use_cloud_server(img_path):
    """ Send image to the cloud server for inference. """
    URL = "https://suite-endpoint-api-apne2.superb-ai.com/endpoints/9a987f3f-174c-4678-acb2-60be9ea6a0ee/inference"
    ACCESS_KEY = "fFJOF6bXM75WTU3qTKADi2DfJRVpcJXk5vAdEep2"

    try:
        with open(img_path, "rb") as image_file:
            image_data = image_file.read()

        response = requests.post(
            url=URL,
            auth=HTTPBasicAuth("kdt2024_1-9", ACCESS_KEY),
            headers={"Content-Type": "image/jpeg"},
            data=image_data,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error uploading {img_path}: {e}")
        return None

def predict_pos(objects_data):
    """ Dummy predict function that returns the same bounding boxes as predictions. """
    predicted_data = []
    for obj in objects_data:
        predicted_data.append({
            "class": obj["class"],
            "box": obj["box"]  # Here, prediction is identical to the ground truth data.
        })
    return predicted_data

def check_objects_in_range(predicted_data, objects_data):
    """ Check if predicted bounding boxes are within the expected ranges. """
    results = []
    for pred, actual in zip(predicted_data, objects_data):
        pred_box = pred["box"]
        actual_box = actual["box"]

        pred_x1, pred_y1, pred_x2, pred_y2 = pred_box
        actual_x1, actual_y1, actual_x2, actual_y2 = actual_box

        is_within_range = (
            actual_x1 >= pred_x1 and actual_y1 >= pred_y1 and
            actual_x2 <= pred_x2 and actual_y2 <= pred_y2
        )
        results.append({
            "class": pred["class"],
            "is_within_range": is_within_range
        })
    return results

def get_img():
    """ Capture an image from the connected camera. """
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

def get_init_data():
    paths = [
        "/Users/jeonsangmin/Desktop/Doosan Rokey 자료/Python_Study/Pico_Defect_Detection/resource/20241108_173716.jpg",
        # path3
        "/Users/jeonsangmin/Desktop/Doosan Rokey 자료/Python_Study/Pico_Defect_Detection/resource/20241108_093331.jpg",
        # path4
        "/Users/jeonsangmin/Desktop/Doosan Rokey 자료/Python_Study/Pico_Defect_Detection/resource/20241108_093725.jpg",
        # path5
        "/Users/jeonsangmin/Desktop/Doosan Rokey 자료/Python_Study/Pico_Defect_Detection/resource/20241108_132649.jpg",
        # path6
        "/Users/jeonsangmin/Desktop/Doosan Rokey 자료/Python_Study/Pico_Defect_Detection/resource/20241108_093323.jpg",
        # path7
        "/Users/jeonsangmin/Desktop/Doosan Rokey 자료/Python_Study/Pico_Defect_Detection/resource/20241108_173747.jpg",
        # path8
        "/Users/jeonsangmin/Desktop/Doosan Rokey 자료/Python_Study/Pico_Defect_Detection/resource/20241108_174343.jpg"
        # path9
    ]

    data = [
        [
            {"class": "RASPBERRY PICO", "box": [74, 269, 241, 147]},
            {"class": "USB", "box": [78, 256, 104, 225]},
        ],
        [
            {"class": "RASPBERRY PICO", "box": [13, 259, 175, 191]},
            {"class": "USB", "box": [13, 240, 33, 216]},
        ],
        [
            {"class": "RASPBERRY PICO", "box": [50, 263, 209, 115]},
            {"class": "USB", "box": [60, 157, 90, 128]},
        ],
        [
            {"class": "RASPBERRY PICO", "box": [113, 242, 182, 81]},
            {"class": "USB", "box": [137, 104, 162, 81]},
        ],
        [
            {"class": "RASPBERRY PICO", "box": [54, 273, 220, 145]},
            {"class": "USB", "box": [185, 192, 216, 163]},
        ],
        [
            {"class": "RASPBERRY PICO", "box": [68, 271, 232, 187]},
            {"class": "USB", "box": [209, 232, 231, 207]},
        ],
        [
            {"class": "RASPBERRY PICO", "box": [102, 256, 193, 90]},
            {"class": "USB", "box": [149, 256, 175, 233]},
        ]
    ]

    return paths, data

def check_pico():
    """ Main function to check and process image and inference data. """
    img = "/Users/jeonsangmin/Desktop/test_img_/test_img_7.jpg"
    data = use_cloud_server(img)

    if data is None:
        print("Error in getting data from the server.")
        return

    # TODO: 컨베이터 코드 + 카메라 이미지 받는 코드 합치지
    # 라즈베리 파이 코드 참고

    Inference_Pico.show_image(data, img_path=img)

    # Simulate confusion matrix processing and distance validation
    centers, objects_data, is_flag = confusion_matrix.process_images(data, "test_img_80.jpg")
    print(centers)
    print(objects_data)

    answer = False

    if is_flag:
        _, _, is_flag = lenght.validate_distances(centers)
        path, data = get_init_data()

        for path, objects_data in zip(path, data):
            print(f"Processing {path}")

            # Predict positions
            predicted_data = predict_pos(objects_data)

            # Check if predicted positions are within the expected range
            results = check_objects_in_range(predicted_data, objects_data)

            # Output results
            for result in results:
                print(f"Class: {result['class']}, Is within range: {result['is_within_range']}")
            print("-" * 50)
            answer = True

        if not answer:
            return

    if not answer:
        print("여기 불량으로 보내는 코드 작성")
        pass

if __name__ == "__main__":
    check_pico()