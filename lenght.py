import math


# 거리 계산 함수
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# 정상품 검증 함수
def validate_distances(centers):
    # 거리 조건 범위
    chipset_bootsel_range = (70, 74.5)
    bootsel_usb_range = (51, 58.5)
    chipset_oscillator_range = (42, 46.5)

    # 필요한 컴포넌트 좌표 가져오기
    chipset_center = centers.get("CHIPSET")
    bootsel_center = centers.get("BOOTSEL")
    usb_center = centers.get("USB")
    oscillator_center = centers.get("OSCILLATOR")

    # 거리 조건 계산
    if chipset_center and bootsel_center:
        chipset_bootsel_distance = calculate_distance(chipset_center, bootsel_center)
        if not (chipset_bootsel_range[0] <= chipset_bootsel_distance <= chipset_bootsel_range[1]):
            return centers, {}, False

    if bootsel_center and usb_center:
        bootsel_usb_distance = calculate_distance(bootsel_center, usb_center)
        if not (bootsel_usb_range[0] <= bootsel_usb_distance <= bootsel_usb_range[1]):
            return centers, {}, False

    if chipset_center and oscillator_center:
        chipset_oscillator_distance = calculate_distance(chipset_center, oscillator_center)
        if not (chipset_oscillator_range[0] <= chipset_oscillator_distance <= chipset_oscillator_range[1]):
            return centers, {}, False
    print("lenght_good")
    # 모든 조건을 만족하면 True 반환
    return centers, {}, True