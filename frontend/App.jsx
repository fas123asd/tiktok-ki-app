import { useState } from "react";
import axios from "axios";

export default function App() {
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState("");
  const [script, setScript] = useState("");

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const res = await axios.post("https://<DEINE-RENDER-URL>/create-video", {
        thema: topic,
      });
      setVideoUrl("https://<DEINE-RENDER-URL>/" + res.data.file);
      setScript(res.data.text);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-6">
      <h1 className="text-2xl font-bold mb-4">🎬 TikTok KI Video Generator</h1>
      <input
        className="p-2 rounded text-black w-full max-w-md mb-4"
        type="text"
        placeholder="Gib ein Thema ein (z.B. Survival, Motivation)"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
      />
      <button
        onClick={handleGenerate}
        disabled={loading || !topic}
        className="bg-green-600 px-4 py-2 rounded mb-6 disabled:opacity-50"
      >
        {loading ? "Generiere..." : "Video erstellen"}
      </button>
      {script && (
        <div className="bg-gray-800 p-4 rounded mb-6 max-w-xl w-full">
          <h2 className="font-semibold mb-2">📜 Skript:</h2>
          <pre className="whitespace-pre-wrap text-sm">{script}</pre>
        </div>
      )}
      {videoUrl && (
        <div className="w-full max-w-md">
          <h2 className="font-semibold mb-2">📹 Vorschau:</h2>
          <video controls src={videoUrl} className="w-full rounded" />
        </div>
      )}
    </main>
  );
}
