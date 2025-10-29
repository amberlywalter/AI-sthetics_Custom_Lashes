from fastapi import APIRouter, UploadFile, File
import tempfile, cv2
from ai.eye_detection import detect_face_landmarks
from ai.shape_analysis import analyze_eye_shape
from ai.lash_recommendation import recommend_lash

router = APIRouter()

@router.post("/analyze_lash/")
async def analyze_lash(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    face, error = detect_face_landmarks(tmp_path)
    if error:
        return {"error": error}

    result = analyze_eye_shape(face)
    lash_style = recommend_lash(result["eye_shape"])

    return {
        "eye_shape": result["eye_shape"],
        "ratio": result["ratio"],
        "predicted_lash_style": lash_style,
        "lash_fit_length_mm": result["lash_fit_length_mm"],
        "reasoning": f"Based on ratio {result['ratio']}, the eyes are classified as {result['eye_shape']}."
    }
