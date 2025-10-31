import Head from "next/head";
import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // ✅ Replace with your Render backend URL
  const API_URL = "https://YOUR-BACKEND-NAME.onrender.com/analyze_lash/";

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a selfie first.");

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data);
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Error analyzing image. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white text-gray-900 flex flex-col items-center justify-center px-6">
      <Head>
        <title>AI-sthetics</title>
        <meta name="description" content="AI-powered lash and eye analysis" />
      </Head>

      <main className="max-w-2xl text-center">
        <h1 className="text-5xl font-bold mb-4">
          Welcome to <span className="text-indigo-600">AI-sthetics</span>
        </h1>
        <p className="text-lg mb-8 text-gray-600">
          Upload a selfie to get a custom AI lash fit based on your unique eye shape.
        </p>

        <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 flex flex-col items-center">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="mb-4"
          />
          <button
            onClick={handleUpload}
            disabled={loading}
            className={`${
              loading ? "bg-gray-400" : "bg-indigo-600 hover:bg-indigo-700"
            } text-white font-semibold py-2 px-6 rounded-xl`}
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>

        {result && (
          <div className="mt-8 bg-gray-50 p-6 rounded-xl shadow-md text-left">
            <h2 className="text-xl font-semibold mb-2 text-indigo-700">
              Analysis Results:
            </h2>
            <p><strong>Eye Shape:</strong> {result.eye_shape}</p>
            <p><strong>Predicted Lash Style:</strong> {result.predicted_lash_style}</p>
            <p><strong>Lash Fit (mm):</strong> Left: {result.lash_fit_length_mm?.left_eye}, Right: {result.lash_fit_length_mm?.right_eye}</p>
            <p><strong>Hooded Eye:</strong> Left: {result.hooded_eye?.left ? "Yes" : "No"}, Right: {result.hooded_eye?.right ? "Yes" : "No"}</p>

            {result.output_image_url && (
              <img
                src={`${API_URL.replace("/analyze_lash/", "")}${result.output_image_url}`}
                alt="AI Analysis"
                className="mt-4 rounded-xl shadow-lg"
              />
            )}
          </div>
        )}
      </main>

      <footer className="mt-12 text-sm text-gray-500">
        &copy; {new Date().getFullYear()} AI-sthetics. All rights reserved.
      </footer>
    </div>
  );
}
