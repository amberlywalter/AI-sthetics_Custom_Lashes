export default function Loader() {
  return (
    <div className="flex items-center justify-center mt-6">
      <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600"></div>
      <p className="ml-3 text-indigo-600 font-medium">Analyzing...</p>
    </div>
  );
}
