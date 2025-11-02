import os
import sys
import uuid
import math
import tempfile
import logging
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# --- Make sure we can import the sibling "ai" package (../ai/*.py) ---
ROOT_DIR = Path(__file__).resolve().parents[1]  # project root (where ai/ and backend/ live)
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from ai.eye_detection import detect_face_landmarks
from ai.shape_analysis import analyze_eye_shape
from ai.lash_recommendation import recommend_lash

# -------------------- App & CORS --------------------
app = FastAPI(title="AI-sthetics Lash Analyzer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",                 # local dev
        "https://ai-sthetics-custom-lashes.vercel.app/",      # <-- replace with your real Vercel URL
        "https://*.vercel.app/", # wildcard for other previre builds
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Logging -----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
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
    # 1) Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Please upload a JPG/PNG/WEBP image.")

    # 2) Read bytes and validate size
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail=f"Image too large. Max {MAX_UPLOAD_MB} MB.")

    # 3) Write to a safe temp file
    suffix = ".jpg"
    if file.filename and "." in file.filename:
        suffix = "." + file.filename.rsplit(".", 1)[-1].lower()
    tmp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        logger.info(f"Received upload: name={file.filename} size={len(data)}B type={file.content_type}")

        # 4) Run AI pipeline
        face, error = detect_face_landmarks(tmp_path)
        if error:
            logger.warning(f"Face/landmarks detection failed: {error}")
            return {"error": error}

        result = analyze_eye_shape(face)
        lash_style = recommend_lash(result["eye_shape"])

        # Optional: add a request ID for debugging
        req_id = uuid.uuid4().hex[:8]
        logger.info(f"[{req_id}] Analysis OK: shape={result['eye_shape']}, style={lash_style}, ratio={result['ratio']}")

        # 5) Return structured response
        return {
            "request_id": req_id,
            "eye_shape": result["eye_shape"],
            "ratio": result["ratio"],
            "lash_fit_length_mm": result["lash_fit_length_mm"],  # {left_eye, right_eye}
            "predicted_lash_style": lash_style,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error during analysis: {e}")
        raise HTTPException(status_code=500, detail="Internal server error. Please try again.")
    finally:
        # 6) Clean up temp file
        if tmp_path and Path(tmp_path).exists():
            try:
                os.remove(tmp_path)
            except Exception as e:
                logger.warning(f"Failed to remove temp file {tmp_path}: {e}")

# Run locally (Render uses its own command/env)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
