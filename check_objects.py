def calculate_relative_position(center1, center2):
    """
    Calculate the relative position of center2 from center1.
    Args:
        center1 (list): The [x, y] center of the reference object (CHIPSET).
        center2 (list): The [x, y] center of the target object.
    Returns:
        tuple: The relative position [x_offset, y_offset].
    """
    if isinstance(center2, list) and len(center2) == 2:  # Ensure it's a list of [x, y]
        x_offset = center2[0] - center1[0]
        y_offset = center2[1] - center1[1]
        return [x_offset, y_offset]
    else:
        raise ValueError(f"Invalid center2 value: {center2}. It should be a list of [x, y].")


def generate_dynamic_expected_positions(centers):
    """
    Generate dynamic expected positions based on the CHIPSET center.
    Args:
        centers (dict): Dictionary of object centers in the image.
    Returns:
        dict: Dynamic expected positions for all objects based on CHIPSET.
    """
    reference_center = centers.get("CHIPSET")
    if not reference_center or not isinstance(reference_center, list) or len(reference_center) != 2:
        raise ValueError("CHIPSET center is missing or has an invalid format. It should be a list of [x, y].")

    expected_positions = {}

    # Iterate through the objects and calculate relative positions
    for class_name, center in centers.items():
        if class_name != "CHIPSET":  # Skip the CHIPSET itself
            if isinstance(center[0], list):  # If it's HOLE with multiple centers
                expected_positions[class_name] = [calculate_relative_position(reference_center, c) for c in center]
            else:  # If it's a single center
                expected_positions[class_name] = calculate_relative_position(reference_center, center)

    return expected_positions


def validate_positions(centers, tolerance=20):
    expected_positions = generate_dynamic_expected_positions(centers)

    # Compare the expected and actual positions
    for class_name, expected_offset in expected_positions.items():
        actual_center = centers.get(class_name)

        if not actual_center:
            return False

        if isinstance(expected_offset, list):  # If expected_offset is a list (like HOLE)
            if len(expected_offset) != len(actual_center):
                return False  # Number of positions do not match

            for i, expected_pos in enumerate(expected_offset):
                if isinstance(expected_pos, list):
                    expected_x, expected_y = expected_pos
                    actual_x, actual_y = actual_center[i]  # Actual center might be a list (for HOLE)
                    if not (abs(actual_x - expected_x) <= tolerance and abs(actual_y - expected_y) <= tolerance):
                        return False
                else:
                    return False  # If the expected position is not a list, something is wrong
        else:
            expected_x, expected_y = expected_offset
            actual_x, actual_y = actual_center
            if not (abs(actual_x - expected_x) <= tolerance and abs(actual_y - expected_y) <= tolerance):
                return False

    return True