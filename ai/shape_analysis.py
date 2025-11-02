import math

def analyze_eye_shape(face):
    """
    Enhanced eye shape analysis using MediaPipe landmarks.
    Incorporates ratios, corner tilt, and eyelid openness for more accurate classification.
    """

    def dist(p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    # Landmarks
    left_outer, left_inner = face.landmark[33], face.landmark[133]
    right_inner, right_outer = face.landmark[362], face.landmark[263]

    # Eye height points
    left_top, left_bottom = face.landmark[159], face.landmark[145]
    right_top, right_bottom = face.landmark[386], face.landmark[374]

    # --- Scale normalization ---
    interpupillary = dist(left_inner, right_inner)
    scale = 63 / interpupillary if interpupillary else 1

    # --- Dimensions ---
    left_width = dist(left_outer, left_inner)
    right_width = dist(right_outer, right_inner)
    left_height = abs(left_top.y - left_bottom.y)
    right_height = abs(right_top.y - right_bottom.y)
    avg_width = (left_width + right_width) / 2
    avg_height = (left_height + right_height) / 2 if right_height else left_height

    # --- Core ratios ---
    ratio = avg_width / avg_height if avg_height else 0
    ratio = round(ratio, 2)
    tilt_angle = abs((left_outer.y - left_inner.y) + (right_outer.y - right_inner.y)) / 2
    tilt_angle = round(tilt_angle * 100, 2)  # simplified tilt proxy

    # --- Shape classification logic ---
    if ratio < 2.0:
        shape = "Round Eyes"
    elif ratio > 3.5 and tilt_angle < 1.0:
        shape = "Monolid / Elongated Eyes"
    elif tilt_angle > 2.0:
        shape = "Upturned or Downturned Eyes"
    elif 2.0 <= ratio <= 3.2:
        shape = "Almond Eyes"
    else:
        shape = "Balanced Eyes"

    # --- Lash fit lengths (scaled mm) ---
    lash_fit_left = round(left_width * scale, 1)
    lash_fit_right = round(right_width * scale, 1)

    return {
        "eye_shape": shape,
        "ratio": ratio,
        "tilt_angle": tilt_angle,
        "scale": round(scale, 2),
        "raw_widths": {"left_eye": round(left_width, 3), "right_eye": round(right_width, 3)},
        "raw_heights": {"left_eye": round(left_height, 3), "right_eye": round(right_height, 3)},
        "lash_fit_length_mm": {"left_eye": lash_fit_left, "right_eye": lash_fit_right},
    }
