import math

def predict_pos(objects_data):
    predicted_data = []
    for obj in objects_data:
        predicted_data.append({
            "class": obj["class"],
            "box": obj["box"]  # Here, prediction is identical to the ground truth data.
        })
    return predicted_data

def check_objects_in_range(predicted_data, objects_data):
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


def validate_positions(centers, positions):
    # 기준점 (CHIPSET과 BOOTSEL) 중심 좌표
    chipset_center = centers['CHIPSET']
    bootsel_center = centers['BOOTSEL']

    # 기준 거리 계산 (CHIPSET과 BOOTSEL 간의 거리)
    reference_distance = math.sqrt(
        (chipset_center[0] - bootsel_center[0]) ** 2 +
        (chipset_center[1] - bootsel_center[1]) ** 2
    )

    # 검증 결과를 저장할 변수
    validation_results = {}
    tolerance = 0.15  # 허용 오차 15%

    # 각 컴포넌트 검증
    for component, position in positions.items():
        if component in ['CHIPSET', 'BOOTSEL']:
            validation_results[component] = True
            continue

        # 상대적 위치 계산
        dx_chipset = (position[0] - chipset_center[0]) / reference_distance
        dy_chipset = (position[1] - chipset_center[1]) / reference_distance
        dx_bootsel = (position[0] - bootsel_center[0]) / reference_distance
        dy_bootsel = (position[1] - bootsel_center[1]) / reference_distance
        relative_pos = {
            'chipset_relative': (dx_chipset, dy_chipset),
            'bootsel_relative': (dx_bootsel, dy_bootsel)
        }

        # 상대적 위치를 동적으로 검증 (여기서 'position'은 각 부품의 실제 위치 데이터)
        # 부품의 이름을 통해 검증할 수 있는 기준을 동적으로 계산
        if component == 'HOLE':
            # 여러 개의 홀에 대해 검증
            valid_holes = 0
            matched_holes = []

            for idx, hole_position in enumerate(position):
                dx_chipset = (hole_position[0] - chipset_center[0]) / reference_distance
                dy_chipset = (hole_position[1] - chipset_center[1]) / reference_distance
                dx_bootsel = (hole_position[0] - bootsel_center[0]) / reference_distance
                dy_bootsel = (hole_position[1] - bootsel_center[1]) / reference_distance
                relative_pos = {
                    'chipset_relative': (dx_chipset, dy_chipset),
                    'bootsel_relative': (dx_bootsel, dy_bootsel)
                }

                # 각 홀의 예상 위치와 비교
                chipset_dx_diff = abs(relative_pos['chipset_relative'][0] - 1.13)
                chipset_dy_diff = abs(relative_pos['chipset_relative'][1] - 0.475)
                bootsel_dx_diff = abs(relative_pos['bootsel_relative'][0] - 0.40)
                bootsel_dy_diff = abs(relative_pos['bootsel_relative'][1] - 0.53)

                # 비교 후 오차가 허용 범위 내인 경우 유효한 홀로 판별
                if (chipset_dx_diff < tolerance and chipset_dy_diff < tolerance and
                        bootsel_dx_diff < tolerance and bootsel_dy_diff < tolerance):
                    valid_holes += 1
                    matched_holes.append(idx)

            validation_results['HOLE'] = valid_holes == 4

        else:
            # 예상된 부품의 상대적 위치 계산
            # 상대적 위치 값은 외부에서 설정하거나 동적으로 계산된 값으로 비교
            expected_chipset_pos = (1.18, 0.195)  # 예시
            expected_bootsel_pos = (0.46, 0.25)  # 예시

            chipset_dx_diff = abs(relative_pos['chipset_relative'][0] - expected_chipset_pos[0])
            chipset_dy_diff = abs(relative_pos['chipset_relative'][1] - expected_chipset_pos[1])
            bootsel_dx_diff = abs(relative_pos['bootsel_relative'][0] - expected_bootsel_pos[0])
            bootsel_dy_diff = abs(relative_pos['bootsel_relative'][1] - expected_bootsel_pos[1])

            # 상대적 위치 차이가 허용 오차 내에 있는지 확인
            validation_results[component] = (chipset_dx_diff < tolerance and
                                             chipset_dy_diff < tolerance and
                                             bootsel_dx_diff < tolerance and
                                             bootsel_dy_diff < tolerance)

    return validation_results
