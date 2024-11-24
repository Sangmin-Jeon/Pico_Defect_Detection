import json
import os
import math

# 거리 계산 함수
def calculate_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points.
    Args:
        point1 (list): [x1, y1]
        point2 (list): [x2, y2]
    Returns:
        float: Distance between the two points.
    """
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# 파일 경로
OUTPUT_CENTER_PATH = "/home/jw7720/두산로보틱스_부트캠프실습3주차/output/center_coordinates.json"
OUTPUT_ALL_DATA_PATH = "/home/jw7720/두산로보틱스_부트캠프실습3주차/output/all_data.json"

# JSON 파일 읽기
with open(OUTPUT_CENTER_PATH, "r") as f:
    center_data = json.load(f)

# 거리 리스트 초기화
chipset_to_bootsel_distances = []
bootsel_to_usb_distances = []
chipset_to_oscillator_distances = []
oscillator_to_bootsel_distances = []

# 거리 계산
for image_name, objects in center_data.items():
    chipset_center = objects.get('CHIPSET')
    bootsel_center = objects.get('BOOTSEL')
    usb_center = objects.get('USB')
    oscillator_center = objects.get('OSCILLATOR')
    
    if chipset_center and bootsel_center:
        distance = calculate_distance(chipset_center, bootsel_center)
        chipset_to_bootsel_distances.append(distance)
    
    if bootsel_center and usb_center:
        distance = calculate_distance(bootsel_center, usb_center)
        bootsel_to_usb_distances.append(distance)
    
    if chipset_center and oscillator_center:
        distance = calculate_distance(chipset_center, oscillator_center)
        chipset_to_oscillator_distances.append(distance)
    
    if oscillator_center and bootsel_center:
        distance = calculate_distance(oscillator_center, bootsel_center)
        oscillator_to_bootsel_distances.append(distance)

# 결과 출력
print("CHIPSET과 BOOTSEL 간의 거리 리스트:", chipset_to_bootsel_distances)
print("BOOTSEL과 USB 간의 거리 리스트:", bootsel_to_usb_distances)
print("CHIPSET과 OSCILLATOR 간의 거리 리스트:", chipset_to_oscillator_distances)
print("OSCILLATOR와 BOOTSEL 간의 거리 리스트:", oscillator_to_bootsel_distances)

# 최솟값과 최댓값 출력
if chipset_to_bootsel_distances:
    print("CHIPSET과 BOOTSEL 간의 최솟값:", min(chipset_to_bootsel_distances))
    print("CHIPSET과 BOOTSEL 간의 최댓값:", max(chipset_to_bootsel_distances))

if bootsel_to_usb_distances:
    print("BOOTSEL과 USB 간의 최솟값:", min(bootsel_to_usb_distances))
    print("BOOTSEL과 USB 간의 최댓값:", max(bootsel_to_usb_distances))

if chipset_to_oscillator_distances:
    print("CHIPSET과 OSCILLATOR 간의 최솟값:", min(chipset_to_oscillator_distances))
    print("CHIPSET과 OSCILLATOR 간의 최댓값:", max(chipset_to_oscillator_distances))

if oscillator_to_bootsel_distances:
    print("OSCILLATOR와 BOOTSEL 간의 최솟값:", min(oscillator_to_bootsel_distances))
    print("OSCILLATOR와 BOOTSEL 간의 최댓값:", max(oscillator_to_bootsel_distances))

# 추가로 all_data.json 파일도 읽기
with open(OUTPUT_ALL_DATA_PATH, "r") as f:
    all_data = json.load(f)

# 읽은 데이터 출력 (주석 처리로 생략)
# print(all_data)