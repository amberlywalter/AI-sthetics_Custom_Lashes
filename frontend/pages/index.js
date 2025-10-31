import Head from "next/head";
import { useState } from "react";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState("");

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
      const res = await fetch("https://ai-sthetics-custom-lashes-backend.onrender.com/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data.result || "No result returned.");
    } catch (error) {
      console.error("Error:", error);
      setResult("Error connecting to backend.");
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

        <div className="border-2 border-dashed border-gray-300 rounded-xl p-8">
          <input type="file" accept="image/*" onChange={handleFileChange} className="mb-4" />
          <button
            onClick={handleAnalyze}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-6 rounded-xl"
          >
            Analyze
          </button>
        </div>

        {result && (
          <p className="mt-6 text-lg text-gray-800 font-medium">
            Result: {result}
          </p>
        )}
      </main>

      <footer className="mt-12 text-sm text-gray-500">
        &copy; {new Date().getFullYear()} AI-sthetics. All rights reserved.
      </footer>
    </div>
  );
}
