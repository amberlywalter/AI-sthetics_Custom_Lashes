import Head from "next/head";
import { useState } from "react";

// Optional loader component inline (you can extract later)
function Loader() {
  return (
    <div className="flex items-center justify-center mt-6">
      <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600"></div>
      <p className="ml-3 text-indigo-600 font-medium">Analyzing...</p>
    </div>
  );
}

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      alert("Please upload a selfie first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setLoading(true);
      setResult(null);

      const res = await fetch("https://ai-sthetics-custom-lashes-backend.onrender.com/analyze_lash/", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (data.error) {
        setResult({ error: data.error });
      } else {
        setResult(data);
      }
    } catch (error) {
      console.error("Error:", error);
      setResult({ error: "Error connecting to backend." });
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

      <main className="max-w-2xl text-center w-full">

        {/* 🟣 Hero Section */}
        <section className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900">
            Discover <span className="text-indigo-600">Your Perfect Lash Fit</span>
          </h1>
          <p className="mt-4 text-lg text-gray-600 max-w-md mx-auto">
            AI-powered analysis designed to match lash styles to your unique eye shape.
          </p>
        </section>

        {/* 🩵 Upload Card */}
        <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 shadow-sm bg-gray-50">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="mb-4 block mx-auto"
          />
          <button
            onClick={handleAnalyze}
            className={`${
              loading ? "bg-gray-400" : "bg-indigo-600 hover:bg-indigo-700"
            } text-white font-semibold py-2 px-6 rounded-xl transition-all`}
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>

          {loading && <Loader />}
        </div>

        {/* 💅 Result Card */}
        {result && !result.error && (
          <div className="mt-10 w-full max-w-md bg-white rounded-2xl shadow-lg p-6 text-left border border-gray-100 mx-auto transition-all duration-500 ease-in-out">
            <h2 className="text-2xl font-semibold text-indigo-700 mb-4">
              Your Lash Fit Analysis
            </h2>
            <p className="mb-2">
              <span className="font-semibold">Eye Shape:</span> {result.eye_shape}
            </p>
            <p className="mb-2">
              <span className="font-semibold">Recommended Style:</span> {result.predicted_lash_style}
            </p>
            <p className="mb-2">
              <span className="font-semibold">Left Lash Fit:</span> {result.lash_fit_length_mm?.left_eye} mm
            </p>
            <p>
              <span className="font-semibold">Right Lash Fit:</span> {result.lash_fit_length_mm?.right_eye} mm
            </p>

            <button
              className="mt-6 w-full bg-indigo-600 text-white py-2 rounded-xl hover:bg-indigo-700 transition-all"
            >
              Shop My Custom Lash
            </button>
          </div>
        )}

        {/* ⚠️ Error message display */}
        {result?.error && (
          <p className="mt-6 text-red-600 font-medium">
            {result.error}
          </p>
        )}
      </main>

      <footer className="mt-12 text-sm text-gray-500">
        &copy; {new Date().getFullYear()} AI-sthetics. All rights reserved.
      </footer>
    </div>
  );
}
