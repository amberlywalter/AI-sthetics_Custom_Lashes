// frontend/pages/index.js
import Head from "next/head";

export default function Home() {
  return (
    <div className="min-h-screen bg-white text-gray-900 flex flex-col items-center justify-center px-6">
      <Head>
        <title>AI-sthetics</title>
        <meta name="description" content="AI-powered lash and eye analysis" />
      </Head>

      <main className="max-w-2xl text-center">
        <h1 className="text-5xl font-bold mb-4">Welcome to <span className="text-indigo-600">AI-sthetics</span></h1>
        <p className="text-lg mb-8 text-gray-600">
          Upload a selfie to get a custom AI lash fit based on your unique eye shape.
        </p>

        <div className="border-2 border-dashed border-gray-300 rounded-xl p-8">
          <input type="file" accept="image/*" className="mb-4" />
          <button className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-6 rounded-xl">
            Analyze
          </button>
        </div>
      </main>

      <footer className="mt-12 text-sm text-gray-500">
        &copy; {new Date().getFullYear()} AI-sthetics. All rights reserved.
      </footer>
    </div>
  );
}
