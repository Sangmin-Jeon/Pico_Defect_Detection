import sqlite3
import os
from datetime import datetime
import confusion_matrix
from lenght import validate_distances

def save_inspection_result(image_data, image_name, is_flag, db_path="inspection_results2.db"):
    # SQLite3 데이터베이스에 연결하거나 없으면 생성
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 기존 테이블 삭제 (이미 존재하는 경우)
    cursor.execute('''DROP TABLE IF EXISTS inspection''')

    # 테이블이 존재하지 않으면 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inspection (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name TEXT NULL,
            image_data BLOB NOT NULL,
            status TEXT NULL,
            timestamp TEXT NULL
        )
    ''')

    # 제품 상태 결정
    status = "good" if is_flag else "bad"

    # 고유한 파일 이름 생성 (타임스탬프 포함)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 이미지 데이터를 BLOB 형태로 저장
    cursor.execute('''
        INSERT INTO inspection (image_name, image_data, status, timestamp) 
        VALUES (?, ?, ?, ?)
    ''', (image_name, image_data, status, timestamp))

    # 변경사항 커밋 및 연결 종료
    conn.commit()
    conn.close()

    print(f"Image saved as {status} product with name {image_name} and timestamp {timestamp}")


# 사용 예시 (main.py)
if __name__ == "__main__":
    # 검사 결과 저장 함수 사용 예시
    # 이미지 데이터를 가져온 후 검사 결과를 저장하는 방식입니다.

    # 추론 이미지 경로와 검사 결과 가져오기
    img = "/home/jw7720/Downloads/test_img_34.jpg"
    image_name = os.path.basename(img)

    with open(img, 'rb') as image_file:
        image_data = image_file.read()

    # 테스트 데이터를 사용하여 데이터 설정
    data = {
        "objects": [
            {"class": "car", "confidence": 0.95, "coordinates": [100, 150, 200, 250]},
            {"class": "person", "confidence": 0.85, "coordinates": [300, 350, 400, 450]}
        ]
    }

    # 데이터가 올바른 형식인 경우만 다음 단계 진행
    if isinstance(data, dict) and "objects" in data:
        centers, objects_data, is_flag = confusion_matrix.process_images(data, "test_img_34.jpg")
        centers, dumi_ob, is_flag = validate_distances(data)
        print(centers, objects_data, is_flag)

        # 검사 결과 저장 함수 호출
        save_inspection_result(image_data, image_name, is_flag)
    else:
        print("Error: The data format is incorrect or missing required keys.")