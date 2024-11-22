from collections import Counter
import cv2


def count_class(detection_data):
    class_cnt = Counter()

    for obj in detection_data.get("objects", []):
        class_number = str(obj["class_number"])
        class_cnt[class_number] += 1

    return class_cnt


def show_image(img_path, detection_data):
    # 이미지 로드
    img = cv2.imread(img_path)
    if img is None:
        print("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
        return

    # 박스 색상과 선 두께 설정
    colors = {
        "1": (0, 255, 0),  # RASPBERRY PICO: 초록색
        "2": (255, 0, 0),  # USB: 파란색
        "3": (0, 0, 255),  # BOOTSEL: 빨간색
        "4": (255, 255, 0),  # OSCILLATOR: 하늘색
        "5": (255, 0, 255),  # CHIPSET: 분홍색
        "6": (0, 255, 255),  # HOLE: 노란색
    }
    thickness = 2

    # 객체 박스 그리기
    for obj in detection_data.get("objects", []):
        class_number = str(obj["class_number"])
        score = obj["confidence"]
        box = obj["bbox"]  # [x1, y1, x2, y2]
        start_point = (int(box[0]), int(box[1]))  # 좌측 상단
        end_point = (int(box[2]), int(box[3]))  # 우측 하단

        # 박스 그리기
        cv2.rectangle(img, start_point, end_point, colors.get(class_number, (255, 255, 255)), thickness)

        # 클래스 이름과 점수 추가
        label = f"Class {class_number} ({score:.2f})"
        label_position = (int(box[0]), int(box[1]) - 10)  # 박스 위 텍스트 위치
        cv2.putText(img, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors.get(class_number, (255, 255, 255)), 1)

    # 클래스별 개수 표시
    class_counts = count_class(detection_data)
    y_offset = 20  # 초기 y 좌표
    for class_num, count in class_counts.items():
        label = f"Class {class_num}: {count}"
        label_position = (10, y_offset)  # 상단에 표시
        cv2.putText(img, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        y_offset += 20  # 텍스트 간격 조정

    # 결과 이미지 표시
    cv2.imshow("Detected Objects", img)
    cv2.waitKey(0)  # 키 입력 대기
    cv2.destroyAllWindows()


def show_imaged(image_path, img_inf_data):
    show_image(image_path, img_inf_data)

    # 클래스 카운트
    class_count = count_class(img_inf_data)

    # 조건 확인: 각 클래스는 1개, HOLE은 4개
    if class_count["1"] == 1 and \
            class_count["2"] == 1 and \
            class_count["3"] == 1 and \
            class_count["4"] == 1 and \
            class_count["5"] == 1 and \
            class_count["6"] == 4:
        print("9개 객체가 맞습니다.")