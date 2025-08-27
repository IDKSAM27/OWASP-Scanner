// src/app/page.tsx (Conceptual Example)
"use client";

import { useState } from "react";

// Define TypeScript types for the API response for full type safety
interface ScanResult {
  vulnerability: string;
  vulnerable: boolean;
  details: string;
}

interface ApiResponse {
  scanUrl: string;
  results: ScanResult[];
}

export default function HomePage() {
  const [url, setUrl] = useState("");
  const [results, setResults] = useState<ApiResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleScan = async () => {
    setIsLoading(true);
    setResults(null);

    const response = await fetch("http://127.0.0.1:5001/api/scan", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });

    const data: ApiResponse = await response.json();
    setResults(data);
    setIsLoading(false);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-900 text-white">
      <div className="container flex flex-col items-center justify-center gap-12 px-4 py-16 ">
        <h1 className="text-5xl font-extrabold tracking-tight">
          Vulnerability <span className="text-[hsl(280,100%,70%)]">Scanner</span>
        </h1>
        
        <div className="flex gap-2">
            <input 
                type="text" 
                value={url} 
                onChange={(e) => setUrl(e.target.value)} 
                placeholder="https://example.com"
                className="w-96 rounded-md bg-gray-800 px-4 py-2 text-white"
            />
            <button 
                onClick={handleScan}
                disabled={isLoading}
                className="rounded-md bg-purple-600 px-4 py-2 font-bold hover:bg-purple-500 disabled:bg-gray-500"
            >
                {isLoading ? "Scanning..." : "Scan"}
            </button>
        </div>

        {/* Results will be displayed here */}
        {results && (
            <div className="mt-8 w-full max-w-2xl">
                {/* We would map over results and display them in styled cards */}
            </div>
        )}
      </div>
    </main>
  );
}
