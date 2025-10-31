from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
from ai.eye_detection import detect_face_landmarks
from ai.shape_analysis import analyze_eye_shape
from ai.lash_recommendation import recommend_lash

app = FastAPI(title="AI-sthetics Lash Analyzer")

# ✅ Allow CORS (frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ai-sthetics-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze_lash/")
async def analyze_lash(file: UploadFile = File(...)):
    # Save the uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(await file.read())
        img_path = tmp.name

    # 1️⃣ Detect landmarks
    face, error = detect_face_landmarks(img_path)
    if error:
        return {"error": error}

    # 2️⃣ Analyze eye shape + measurements
    result = analyze_eye_shape(face)

    # 3️⃣ Get lash style recommendation
    lash_style = recommend_lash(result["eye_shape"])

    # 4️⃣ Combine and return
    return {
        "eye_shape": result["eye_shape"],
        "ratio": result["ratio"],
        "lash_fit_length_mm": result["lash_fit_length_mm"],
        "predicted_lash_style": lash_style,
    }

@app.get("/")
def root():
    return {"message": "AI-sthetics Backend is Live!"}
