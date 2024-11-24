import json
import os
import requests
from requests.auth import HTTPBasicAuth


# 중심점 계산 함수
def calculate_center(box):
    x_min, y_min, x_max, y_max = box
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    return x_center, y_center


# 디렉토리에 결과 저장 함수
def save_json(output_path, data):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 객체 개수 검증 함수
def validate_counts(detected_classes, required_counts):
    detected_counts = {}
    for obj in detected_classes:
        cls = obj["class"]
        detected_counts[cls] = detected_counts.get(cls, 0) + 1

    for cls, count in required_counts.items():
        if detected_counts.get(cls, 0) != count:
            return False
    return True


# API 요청 함수
def make_api_request(image_path, url, auth):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    response = requests.post(
        url=url,
        auth=auth,
        headers={"Content-Type": "image/jpeg"},
        data=image_data,
    )
    return response.json()


# 중심점 및 전체 데이터 생성 함수
def process_detected_classes(detected_classes):
    centers = {}
    hole_centers = []  # HOLE 중심점을 수집할 리스트
    objects_data = []

    for obj in detected_classes:
        class_name = obj["class"]
        center_x, center_y = calculate_center(obj["box"])

        if class_name == "HOLE":
            hole_centers.append([center_x, center_y])  # HOLE 중심점 추가
        else:
            centers[class_name] = [center_x, center_y]

        objects_data.append({
            "class": class_name,
            "score": round(obj["score"], 3),
            "box": obj["box"]
        })

    if hole_centers:  # HOLE 데이터가 있다면 추가
        centers["HOLE"] = hole_centers

    return centers, objects_data


# 전체 데이터 처리 함수
def process_images(response, img_name):
    required_counts = {
        "RASPBERRY PICO": 1,
        "BOOTSEL": 1,
        "CHIPSET": 1,
        "OSCILLATOR": 1,
        "USB": 1,
        "HOLE": 4
    }

    center_data = {}  # 중심점 데이터
    all_data = {}  # 전체 데이터
    detected_classes = response.get("objects", [])

    # 객체 개수 검증
    if not validate_counts(detected_classes, required_counts):
        print(f"{img_name}는 요구 조건을 충족하지 못했습니다. 제외합니다.")
        return None, None, False

    # 중심점 및 전체 데이터 생성
    centers, objects_data = process_detected_classes(detected_classes)

    # # 데이터 저장
    # center_data[file_name] = centers
    # all_data[file_name] = objects_data

    # JSON 파일 저장
    # save_json(output_center_path, center_data)
    # save_json(output_all_data_path, all_data)

    return centers, objects_data, True
