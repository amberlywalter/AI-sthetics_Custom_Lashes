import math

def analyze_eye_shape(face, debug=False):
    """
    Analyze eye landmarks from MediaPipe FaceMesh using lash technician logic.
    Detects structural eye shape and lash mapping metrics such as symmetry,
    lid exposure, and natural lift — but does NOT assign lash styles.
    """

    def dist(p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    # --- Core facial landmarks ---
    left_outer, left_inner = face.landmark[33], face.landmark[133]
    right_inner, right_outer = face.landmark[362], face.landmark[263]
    left_top, left_bottom = face.landmark[159], face.landmark[145]
    right_top, right_bottom = face.landmark[386], face.landmark[374]

    # --- Measure and normalize ---
    interpupillary = dist(left_inner, right_inner)
    scale = 63 / interpupillary if interpupillary else 1  # normalize to 63mm avg
    left_width = dist(left_outer, left_inner)
    right_width = dist(right_outer, right_inner)
    left_height = abs(left_top.y - left_bottom.y)
    right_height = abs(right_top.y - right_bottom.y)

    avg_width = (left_width + right_width) / 2
    avg_height = (left_height + right_height) / 2 if right_height else left_height

    ratio = avg_width / avg_height if avg_height else 0
    ratio = round(ratio, 2)
    openness = avg_height * scale * 100  # estimated visible lid opening (mm)
    openness = round(openness, 2)
    tilt_angle = abs((left_outer.y - left_inner.y) + (right_outer.y - right_inner.y)) / 2
    tilt_angle = round(tilt_angle * 100, 2)

    # --- Real lash technician–inspired metrics ---
    # Eyelid exposure: how much lid skin is visible above lash line
    eyelid_exposure = "Low" if openness < 6 else "Moderate" if openness < 9 else "High"

    # Symmetry: horizontal alignment of outer vs inner corners
    asymmetry = abs((left_outer.y - right_outer.y) - (left_inner.y - right_inner.y)) * 100
    symmetry_score = "Balanced" if asymmetry < 1.5 else "Slight Asymmetry" if asymmetry < 3 else "Visible Asymmetry"

    # Curl visibility: helps determine if eyes appear “deep set” or “projected”
    projection_ratio = round((avg_width / interpupillary) * 100, 2)
    projection_type = (
        "Deep Set" if projection_ratio < 40 else
        "Average Depth" if projection_ratio < 50 else
        "Projected / Prominent"
    )

    # --- Eye shape logic (pure structural classification) ---
    if ratio < 1.8 and openness > 10:
        eye_shape = "Round Eyes"
    elif 1.8 <= ratio <= 3.2 and openness > 7:
        eye_shape = "Almond Eyes"
    elif tilt_angle > 2.5:
        eye_shape = "Downturned / Upturned Eyes"
    elif openness < 6.5:
        eye_shape = "Monolid (Low Eyelid Crease)"
    else:
        eye_shape = "Balanced Eyes"

    # --- Output ---
    result = {
        "eye_shape": eye_shape,
        "ratio": ratio,
        "openness_mm": openness,
        "eyelid_exposure": eyelid_exposure,
        "symmetry_score": symmetry_score,
        "projection_type": projection_type,
        "tilt_angle_deg": tilt_angle,
        "scale_factor": round(scale, 2),
        "lash_fit_length_mm": {
            "left_eye": round(left_width * scale, 1),
            "right_eye": round(right_width * scale, 1)
        }
    }

    if debug:
        print("\n👁️ Detailed Eye Analysis:")
        for k, v in result.items():
            print(f"  {k}: {v}")
        print("-" * 40)

    return result
