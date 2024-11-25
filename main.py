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
    x = size_dict["x"]
    y = size_dict["y"]
    w = size_dict["width"]
    h = size_dict["height"]
    return img[y:y + h, x:x + w]


def use_cloud_server(img_path):
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


def get_init_data():
    return [
        [
            {"class": "RASPBERRY PICO", "box": [120, 159, 251, 429]},
            {"class": "USB", "box": [147, 394, 191, 434]},
        ],
        [
            {"class": "RASPBERRY PICO", "box": [143, 124, 405, 369]},
            {"class": "USB", "box": [155, 295, 210, 350]},
        ],
        [
            {"class": "RASPBERRY PICO", "box": [111, 256, 386, 389]},
            {"class": "USB", "box": [111, 289, 154, 332]},
        ],
        [
            {"class": "RASPBERRY PICO", "box": [122, 168, 381, 417]},
            {"class": "USB", "box": [133, 187, 190, 241]},
        ],
        [
            {"class": "RASPBERRY PICO", "box": [295, 99, 419, 368]},
            {"class": "USB", "box": [342, 97, 387, 137]},
        ],
        [
            {"class": "RASPBERRY PICO", "box": [107, 256, 381, 396]},
            {"class": "USB", "box": [343, 319, 383, 366]},
        ],
        [
            {"class": "RASPBERRY PICO", "box": [192, 104, 406, 379]},
            {"class": "USB", "box": [327, 322, 381, 371]},
        ],
    ]



# 중심점이 박스 안에 있거나 걸치는지 확인.
def is_point_in_or_touching_box(center_point, box):
    x_center, y_center = center_point
    x1, y1, x2, y2 = box

    # 점이 박스 내부에 있는 경우
    if x1 <= x_center <= x2 and y1 <= y_center <= y2:
        return True

    # 점이 박스를 걸치는 경우: 확장된 영역 확인 (반경 5 픽셀 예시)
    buffer = 5
    expanded_box = [x1 - buffer, y1 - buffer, x2 + buffer, y2 + buffer]
    return (
        expanded_box[0] <= x_center <= expanded_box[2]
        and expanded_box[1] <= y_center <= expanded_box[3]
    )

# 중심점이 데이터의 박스와 매칭되는지 확인.
def match_center_with_boxes(centers, data):
    for center_class, center_value in centers.items():
        # HOLE은 체크하지 않음
        if center_class == "HOLE":
            continue  # HOLE은 건너뛰기
        else:
            # 다른 객체들에 대해서 매칭 수행
            matched = any(
                is_point_in_or_touching_box(center_value, obj["box"])
                for obj in data
                if obj["class"] == center_class
            )
            if not matched:
                return False
    return True

# 예측된 결과를 이미지에 시각적으로 표시.
def visualize_ret(image, ret):
    # 이미지 파일을 읽어오는 부분 (이미지가 경로로 전달되지 않으면, 이미지 경로를 여기에 추가)
    img = cv2.imread(image)  # 이미지 파일을 읽어서 `img`에 저장

    for item in ret:
        box = item["box"]

        # box는 [x1, y1, x2, y2] 형태로 되어 있으므로, (x1, y1), (x2, y2)로 처리
        if len(box) == 4:
            pt1 = (int(box[0]), int(box[1]))  # 왼쪽 위 꼭지점 (x1, y1)
            pt2 = (int(box[2]), int(box[3]))  # 오른쪽 아래 꼭지점 (x2, y2)

            # 사각형 그리기
            cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
        else:
            print(f"Invalid box format: {box}")

    # 결과 이미지 출력 (예시)
    cv2.imshow("Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 예측된 좌표를 이미지의 USB 좌표에 맞게 이동시킴.
def adjust_coordinates_for_usb(ret, img_usb_center):
    # 예측된 USB 좌표 찾기
    predicted_usb = None
    for item in ret:
        if item["class"] == "USB":
            predicted_usb = item["box"]
            break

    if predicted_usb is None:
        print("No USB detected in the prediction.")
        return ret

    # 예측된 USB의 중심 계산
    predicted_x1, predicted_y1, predicted_x2, predicted_y2 = predicted_usb
    predicted_center_x = (predicted_x1 + predicted_x2) / 2
    predicted_center_y = (predicted_y1 + predicted_y2) / 2

    # 이미지의 USB 중심 좌표와 예측된 중심 좌표 차이 계산
    center_dx = img_usb_center[0] - predicted_center_x
    center_dy = img_usb_center[1] - predicted_center_y

    # ret에서 모든 좌표를 이동시킴
    for item in ret:
        item_x1, item_y1, item_x2, item_y2 = item["box"]
        # 모든 박스를 이동시키기
        item["box"] = [
            item_x1 + center_dx,
            item_y1 + center_dy,
            item_x2 + center_dx,
            item_y2 + center_dy,
        ]

    return ret

def check_pico():
    img = "/Users/jeonsangmin/Desktop/test_img_/test_img_94.jpg"
    data = use_cloud_server(img)

    if data is None:
        print("Error in getting data from the server.")
        return

    centers, objects_data, is_flag = confusion_matrix.process_images(data, "test_img_14.jpg")
    print(centers)
    print(objects_data)

    if is_flag:
        _, _, is_flag = lenght.validate_distances(centers)
        data = get_init_data()

        for i in range(len(data)):
            input_data = data[i]
            ret = check_objects.predict_pos(input_data)
            print(ret)

            usb_value = centers['USB']
            # 중심 좌표를 사용하여 보정
            _ret = adjust_coordinates_for_usb(ret, usb_value)

            if match_center_with_boxes(centers, _ret):
                visualize_ret(img, _ret)
                print(f"양품 입니다: {img}")
                break
            else:
                print(f"불량 입니다: {img}")


if __name__ == "__main__":
    check_pico()
