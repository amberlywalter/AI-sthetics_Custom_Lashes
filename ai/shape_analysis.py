import math

def analyze_eye_shape(face):
    """
    Analyze eye landmarks from MediaPipe face mesh and classify eye shape.
    Returns ratio, scale, and lash fit lengths for both eyes.
    """

    # --- Helper to compute Euclidean distance between two landmarks ---
    def dist(p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    # --- Key landmark indices (MediaPipe FaceMesh) ---
    left_outer, left_inner = face.landmark[33], face.landmark[133]
    right_inner, right_outer = face.landmark[362], face.landmark[263]

    # --- Calculate interpupillary distance for scale normalization ---
    interpupillary = dist(left_inner, right_inner)
    scale = 63 / interpupillary if interpupillary else 1  # 63 mm average

    # --- Eye widths ---
    left_eye_width = dist(left_outer, left_inner)
    right_eye_width = dist(right_outer, right_inner)

    # --- Eye heights ---
    left_height = abs(face.landmark[159].y - face.landmark[145].y)
    right_height = abs(face.landmark[386].y - face.landmark[374].y)
    avg_height = (left_height + right_height) / 2 if right_height else left_height

    # --- Compute ratio (width ÷ height) with clamping ---
    ratio = (left_eye_width + right_eye_width) / (2 * avg_height) if avg_height else 0
    ratio = max(1.0, min(ratio, 5.0))  # clamp to reasonable human range

    # --- Classify shape ---
    if ratio > 3.0:
        shape = "Almond Eyes"
    elif ratio < 2.0:
        shape = "Round Eyes"
    else:
        shape = "Balanced Eyes"

    # --- Compute lash fit length in mm (scaled) ---
    lash_fit_left = round(left_eye_width * scale, 1)
    lash_fit_right = round(right_eye_width * scale, 1)

    # --- Return structured results ---
    return {
        "eye_shape": shape,
        "ratio": round(ratio, 2),
        "scale": round(scale, 2),
        "raw_widths": {
            "left_eye": round(left_eye_width, 3),
            "right_eye": round(right_eye_width, 3),
        },
        "raw_heights": {
            "left_eye": round(left_height, 3),
            "right_eye": round(right_height, 3),
        },
        "lash_fit_length_mm": {
            "left_eye": lash_fit_left,
            "right_eye": lash_fit_right,
        },
    }
