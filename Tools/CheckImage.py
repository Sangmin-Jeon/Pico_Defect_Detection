import requests
from requests.auth import HTTPBasicAuth
import os
from collections import Counter
import cv2


def count_class(detection_data):
    class_cnt = {
        "RASPBERRY PICO": 0,
        "USB": 0,
        "BOOTSEL": 0,
        "OSCILLATOR": 0,
        "CHIPSET": 0,
        "HOLE": 0,
    }

    for obj in detection_data["objects"]:
        class_name = obj["class"]
        if class_name in class_cnt:
            class_cnt[class_name] += 1
        else:
            class_cnt[class_name] = 1  # 새로운 클래스 처리

    return class_cnt



def show_image(img_path, detection_data):
    # 이미지 로드
    img = cv2.imread(img_path)
    if img is None:
        print("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
        return

    # 박스 색상과 선 두께 설정
    colors = {
        "RASPBERRY PICO": (0, 255, 0),  # 초록색
        "USB": (255, 0, 0),  # 파란색
        "BOOTSEL": (0, 0, 255),  # 빨간색
        "OSCILLATOR": (255, 255, 0),  # 하늘색
        "CHIPSET": (255, 0, 255),  # 분홍색
        "HOLE": (0, 255, 255),  # 노란색
    }
    thickness = 2

    # 객체 박스 그리기
    for obj in detection_data["objects"]:
        class_name = obj["class"]
        score = obj["score"]
        box = obj["box"]  # [x1, y1, x2, y2]
        start_point = (box[0], box[1])  # 좌측 상단
        end_point = (box[2], box[3])  # 우측 하단

        # 박스 그리기
        cv2.rectangle(img, start_point, end_point, colors.get(class_name, (255, 255, 255)), thickness)

        # 클래스 이름과 점수 추가
        label = f"{class_name} ({score:.2f})"
        label_position = (box[0], box[1] - 10)  # 박스 위 텍스트 위치
        cv2.putText(img, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors.get(class_name, (255, 255, 255)),
                    1)

    # 클래스별 개수 표시
    class_counts = count_class(detection_data)
    width_offset = 10  # 초기 x 좌표
    for key, value in class_counts.items():  # 'items()' 메서드를 사용하여 key-value 쌍을 순회
        label = f"{key}: {value}"
        label_position = (width_offset, 20)  # 상단에 표시
        cv2.putText(img, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        width_offset += 150  # 텍스트 간격 조정

    # 결과 이미지 표시
    cv2.imshow("Detected Objects", img)
    cv2.waitKey(0)  # 키 입력 대기
    cv2.destroyAllWindows()


def show_imaged(directory_path, URL, ACCESS_KEY):
    # 파일 목록 가져오기
    file_list = os.listdir(directory_path)

    # 파일 처리
    for img in file_list:
        image_path = os.path.join(directory_path, img)

        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        try:
            response = requests.post(
                url=URL,
                auth=HTTPBasicAuth("kdt2024_1-9", ACCESS_KEY),
                headers={"Content-Type": "image/jpeg"},
                data=image_data,
            )
            # 응답 출력
            print(f"File: {img}, Response: {response.status_code}, Data: {response.json()}")
            show_image(image_path, response.json())

            # 'objects'에서 각 클래스 카운트 계산
            class_count = Counter([obj['class'] for obj in response.json()['objects']])

            # # 조건 확인: 각 클래스는 1개, HOLE은 4개
            if class_count['RASPBERRY PICO'] == 1 and \
               class_count['USB'] == 1 and \
               class_count['BOOTSEL'] == 1 and \
               class_count['OSCILLATOR'] == 1 and \
               class_count['CHIPSET'] == 1 and \
               class_count['HOLE'] == 4:
                print(f"9개 객체가 맞습니다: {img}")

        except requests.RequestException as e:
            print(f"Error uploading {img}: {e}")