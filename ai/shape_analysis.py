import math

def analyze_eye_shape(face):
    # Helper
    def dist(p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    left_outer, left_inner = face.landmark[33], face.landmark[133]
    right_inner, right_outer = face.landmark[362], face.landmark[263]
    interpupillary = dist(left_inner, right_inner)
    scale = 63 / interpupillary if interpupillary else 1

    left_eye_width = dist(left_outer, left_inner)
    right_eye_width = dist(right_outer, right_inner)

    left_height = abs(face.landmark[159].y - face.landmark[145].y)
    ratio = left_eye_width / left_height if left_height else 0

    if ratio > 3.0:
        shape = "Almond Eyes"
    elif ratio < 2.0:
        shape = "Round Eyes"
    else:
        shape = "Balanced Eyes"

    return {
        "eye_shape": shape,
        "ratio": round(ratio, 2),
        "scale": round(scale, 1),
        "lash_fit_length_mm": {
            "left_eye": round(left_eye_width * scale, 1),
            "right_eye": round(right_eye_width * scale, 1)
        }
    }
