import math

def analyze_eye_shape(face, debug=False):
    """
    Improved eye shape classification with better ratio thresholds,
    reduced false monolid classifications, and additional openness metric.
    """

    def dist(p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    # Landmarks
    left_outer, left_inner = face.landmark[33], face.landmark[133]
    right_inner, right_outer = face.landmark[362], face.landmark[263]
    left_top, left_bottom = face.landmark[159], face.landmark[145]
    right_top, right_bottom = face.landmark[386], face.landmark[374]

    # Interpupillary scale (mm normalization)
    interpupillary = dist(left_inner, right_inner)
    scale = 63 / interpupillary if interpupillary else 1

    # Eye geometry
    left_width = dist(left_outer, left_inner)
    right_width = dist(right_outer, right_inner)
    left_height = abs(left_top.y - left_bottom.y)
    right_height = abs(right_top.y - right_bottom.y)
    avg_width = (left_width + right_width) / 2
    avg_height = (left_height + right_height) / 2 if right_height else left_height

    # Core metrics
    ratio = avg_width / avg_height if avg_height else 0
    ratio = round(ratio, 2)

    # Measure how "open" the eyes are (height relative to scale)
    openness = avg_height * scale * 100  # approximate openness in mm
    openness = round(openness, 2)

    # Vertical tilt between outer and inner corners
    tilt_angle = abs((left_outer.y - left_inner.y) + (right_outer.y - right_inner.y)) / 2
    tilt_angle = round(tilt_angle * 100, 2)

    # Classification (tuned thresholds)
    if ratio < 1.8 and openness > 10:
        shape = "Round Eyes"
    elif 1.8 <= ratio <= 3.2 and openness > 7:
        shape = "Almond Eyes"
    elif tilt_angle > 2.5:
        shape = "Upturned / Downturned Eyes"
    elif openness < 6.5:
        shape = "Monolid (Low Eyelid Crease)"
    else:
        shape = "Balanced Eyes"

    # Lash fit estimates
    lash_fit_left = round(left_width * scale, 1)
    lash_fit_right = round(right_width * scale, 1)

    result = {
        "eye_shape": shape,
        "ratio": ratio,
        "tilt_angle": tilt_angle,
        "openness": openness,
        "scale": round(scale, 2),
        "lash_fit_length_mm": {
            "left_eye": lash_fit_left,
            "right_eye": lash_fit_right
        }
    }

    if debug:
        print("\n🧠 Debug Eye Analysis:")
        for k, v in result.items():
            print(f"  {k}: {v}")
        print("-" * 40)

    return result
