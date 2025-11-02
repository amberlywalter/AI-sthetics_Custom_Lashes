import os
import sys
import uuid
import math
import tempfile
import logging
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

import cv2
import mediapipe as mp

# --- Ensure imports for ai modules (../ai/*.py) ---
ROOT_DIR = Path(__file__).resolve().parents[1]  # project root (where ai/ and backend/ live)
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from ai.eye_detection import detect_face_landmarks
from ai.shape_analysis import analyze_eye_shape
from ai.lash_recommendation import recommend_lash

# -------------------- App & CORS --------------------
app = FastAPI(title="AI-sthetics Lash Analyzer", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ai-sthetics-custom-lashes.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Logging -----------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("ai-sthetics")

# -------------------- Settings ----------------------
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/jpg", "image/webp"}
MAX_UPLOAD_MB = 10
MAX_BYTES = MAX_UPLOAD_MB * 1024 * 1024

# -------------------- Routes ------------------------
@app.get("/")
def root():
    return {"message": "AI-sthetics Backend is Live!", "version": app.version}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze_lash/")
async def analyze_lash(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Please upload a JPG/PNG/WEBP image.")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail=f"Image too large. Max {MAX_UPLOAD_MB} MB.")

    suffix = Path(file.filename).suffix or ".jpg"
    tmp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        logger.info(f"Received upload: {file.filename}, size={len(data)}B, type={file.content_type}")

        face, error = detect_face_landmarks(tmp_path)
        if error:
            logger.warning(f"Face/landmark detection failed: {error}")
            return JSONResponse(content={"error": error}, status_code=400)

        analysis = analyze_eye_shape(face)
        recommendation = recommend_lash(analysis)

        req_id = uuid.uuid4().hex[:8]
        logger.info(f"[{req_id}] Analysis OK | Shape={analysis['eye_shape']}")

        return JSONResponse(
            content={
                "request_id": req_id,
                "status": "success",
                "analysis": analysis,
                "recommendation": recommendation,
            },
            status_code=200,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error during analysis: {e}")
        raise HTTPException(status_code=500, detail="Internal server error. Please try again.")
    finally:
        if tmp_path and Path(tmp_path).exists():
            try:
                os.remove(tmp_path)
            except Exception as e:
                logger.warning(f"Failed to remove temp file {tmp_path}: {e}")


# -------------------- Debug Visualization --------------------
@app.post("/debug_analysis/")
async def debug_analysis(file: UploadFile = File(...)):
    """
    Generates an annotated image showing detected face mesh and eyes.
    Returns the processed file for visual debugging.
    """
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    suffix = Path(file.filename).suffix or ".jpg"
    tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp_in.write(data)
    tmp_in.close()

    tmp_out_path = f"{tmp_in.name}_annotated.jpg"

    try:
        mp_face_mesh = mp.solutions.face_mesh
        image = cv2.imread(tmp_in.name)
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file.")

        with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.6,
        ) as face_mesh:
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            if not results.multi_face_landmarks:
                raise HTTPException(status_code=400, detail="No face detected in image.")

            for face_landmarks in results.multi_face_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    image,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_CONTOURS,
                    mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style(),
                    mp.solutions.drawing_styles.get_default_face_mesh_contours_style(),
                )

        cv2.imwrite(tmp_out_path, image)
        logger.info(f"Generated annotated image: {tmp_out_path}")
        return FileResponse(tmp_out_path, media_type="image/jpeg")

    except Exception as e:
        logger.exception(f"Error during debug visualization: {e}")
        raise HTTPException(status_code=500, detail="Error generating debug image.")
    finally:
        for path in [tmp_in.name]:
            if os.path.exists(path):
                os.remove(path)


# -------------------- Run Locally --------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
