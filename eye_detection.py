import cv2
import mediapipe as mp
import math
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

def analyze_eye_shape(image_path, output_path="output_lash_hooded.jpg"):
    image = cv2.imread(image_path)
    if image is None:
        return {"error": "Image not found."}

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    if not results.multi_face_landmarks:
        return {"error": "No face detected."}

    face = results.multi_face_landmarks[0]
    h, w, _ = image.shape

    # Convert normalized landmark to pixel
    def lm_to_pixel(lm):
        return int(lm.x * w), int(lm.y * h)

    # Eye corners for width measurement
    left_outer = lm_to_pixel(face.landmark[33])
    left_inner = lm_to_pixel(face.landmark[133])
    right_outer = lm_to_pixel(face.landmark[263])
    right_inner = lm_to_pixel(face.landmark[362])

    # Upper eyelid points for lash line
    left_lash_pts = [33, 160, 159, 158, 157, 173, 133]
    right_lash_pts = [362, 385, 386, 387, 388, 466, 263]

    # Distance function (pixels)
    def dist(p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    left_width = dist(left_outer, left_inner)
    right_width = dist(right_outer, right_inner)
    interpupillary = dist(left_inner, right_inner)

    # Scale to mm
    scale = 63 / interpupillary
    left_lash_mm = left_width * scale
    right_lash_mm = right_width * scale

    # Eye height for ratio
    left_top = lm_to_pixel(face.landmark[159])
    left_bottom = lm_to_pixel(face.landmark[145])
    right_top = lm_to_pixel(face.landmark[386])
    right_bottom = lm_to_pixel(face.landmark[374])

    left_height = abs(left_top[1] - left_bottom[1])
    right_height = abs(right_top[1] - right_bottom[1])
    left_ratio = left_width / left_height if left_height != 0 else 0
    right_ratio = right_width / right_height if right_height != 0 else 0
    avg_ratio = (left_ratio + right_ratio)/2

    # Determine basic lash style
    if avg_ratio > 3.0:
        shape = "Almond Eyes"
        recommendation = "Cat-Eye or Wispy Lash"
        reasoning = "Almond eyes are elongated, so cat-eye or wispy lashes enhance their natural shape and provide a lifted effect."
        curve_factor = 0.3
    elif avg_ratio < 2.0:
        shape = "Round Eyes"
        recommendation = "Natural or Doll Style Lash"
        reasoning = "Round eyes benefit from natural or doll-style lashes to add length without making the eyes look overly wide."
        curve_factor = 0.15
    else:
        shape = "Balanced Eyes"
        recommendation = "Classic or Hybrid Lash"
        reasoning = "Balanced eyes work well with classic or hybrid lashes for a natural, harmonious look."
        curve_factor = 0.2

    # Hooded eye detection
    # Left eye fold: 65 (brow) to upper eyelid 159
    left_fold_height = abs(face.landmark[65].y - face.landmark[159].y)
    left_visible_height = abs(face.landmark[159].y - face.landmark[145].y)
    is_hooded_left = left_fold_height / left_visible_height < 0.5  # threshold

    # Right eye fold: 295 (brow) to upper eyelid 386
    right_fold_height = abs(face.landmark[295].y - face.landmark[386].y)
    right_visible_height = abs(face.landmark[386].y - face.landmark[374].y)
    is_hooded_right = right_fold_height / right_visible_height < 0.5

    if is_hooded_left or is_hooded_right:
        recommendation += " (Hooded eyes: emphasize outer corner, use curled lashes)"
        reasoning += " Hooded eyes benefit from curled lashes and emphasis on the outer corners to open the eye."

    # Draw lash along eyelid
    def draw_lash_line(img, lm_list, offset=0, color=(0,0,255), thickness=2):
        points = []
        for idx in lm_list:
            x, y = lm_to_pixel(face.landmark[idx])
            points.append([x, y - offset])  # offset slightly above eyelid
        points = np.array(points, np.int32).reshape((-1,1,2))
        cv2.polylines(img, [points], False, color, thickness, cv2.LINE_AA)

    draw_lash_line(image, left_lash_pts, offset=3)
    draw_lash_line(image, right_lash_pts, offset=3)

    # Add text
    cv2.putText(image, f"{recommendation}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
    cv2.putText(image, f"Reason: {reasoning}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
    cv2.putText(image, f"Left Lash: {round(left_lash_mm,1)}mm", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    cv2.putText(image, f"Right Lash: {round(right_lash_mm,1)}mm", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    cv2.imwrite(output_path, image)

    return {
        "eye_shape": shape,
        "ratio": round(avg_ratio,2),
        "recommended_style": recommendation,
        "reasoning": reasoning,
        "hooded_eye": {
            "left": is_hooded_left,
            "right": is_hooded_right
        },
        "lash_fit_length_mm": {
            "left_eye": round(left_lash_mm,1),
            "right_eye": round(right_lash_mm,1)
        },
        "scale_based_on_IPD_mm": round(scale,1),
        "output_image": output_path
    }

if __name__ == "__main__":
    result = analyze_eye_shape("77AE8E7F-8985-40D8-B6CF-829AC8A54448.jpeg")
    print(result)
