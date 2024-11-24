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
        "RASPBERRY PICO": (0, 255, 0),  # 초록색
        "USB": (255, 0, 0),  # 파란색
        "BOOTSEL": (0, 0, 255),  # 빨간색
        "OSCILLATOR": (255, 255, 0),  # 하늘색
        "CHIPSET": (255, 0, 255),  # 분홍색
        "HOLE": (0, 255, 255),  # 노란색
    }
    thickness = 2

    # 객체 박스 그리기
    for obj in detection_data.get("objects", []):
        class_name = obj["class"]
        score = obj["score"]  # confidence를 score로 수정
        box = obj["box"]  # bbox를 box로 수정
        start_point = (int(box[0]), int(box[1]))  # 좌측 상단
        end_point = (int(box[2]), int(box[3]))  # 우측 하단

        # 박스 그리기
        cv2.rectangle(img, start_point, end_point, colors.get(class_name, (255, 255, 255)), thickness)

        # 클래스 이름과 점수 추가
        label = f"{class_name} ({score:.2f})"
        label_position = (int(box[0]), int(box[1]) - 10)  # 박스 위 텍스트 위치
        cv2.putText(img, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors.get(class_name, (255, 255, 255)),
                    1)
    # 클래스별 개수 표시
    # class_counts = count_class(detection_data)
    # y_offset = 20  # 초기 y 좌표
    # for class_name, count in class_counts.items():
    #     label = f"{class_name}: {count}"
    #     label_position = (10, y_offset)  # 상단에 표시
    #     cv2.putText(img, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    #     y_offset += 20  # 텍스트 간격 조정

    # 결과 이미지 표시
    cv2.imshow("Detected Objects", img)
    cv2.waitKey(0)  # 키 입력 대기
    cv2.destroyAllWindows()