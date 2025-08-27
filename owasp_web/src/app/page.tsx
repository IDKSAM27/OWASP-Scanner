"use client";

import { useState } from "react";

interface ScanResult {
  vulnerability: string;
  vulnerable: boolean;
  details: string;
}

interface ApiResponse {
  url: string;
  results: ScanResult[];
  error?: string;
}

export default function HomePage() {
  const [url, setUrl] = useState<string>("");
  const [results, setResults] = useState<ScanResult[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleScan = async () => {
    if (!url.trim()) {
      setError("Please enter a URL");
      return;
    }

    setIsLoading(true);
    setError(null);
    setResults([]);

    try {
      console.log("Sending request to:", "http://localhost:5001/api/scan");
      console.log("Request body:", { url });
      
      const response = await fetch("http://localhost:5001/api/scan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      console.log("Response status:", response.status);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ApiResponse = await response.json();
      console.log("Response data:", data);
      
      if (data.error) {
        setError(data.error);
      } else {
        setResults(data.results || []);
      }
    } catch (err) {
      console.error("Fetch error:", err);
      setError(err instanceof Error ? err.message : "An unknown error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-900 text-white">
      <div className="container flex flex-col items-center justify-center gap-12 px-4 py-16">
        <h1 className="text-5xl font-extrabold tracking-tight">
          Vulnerability <span className="text-purple-400">Scanner</span>
        </h1>
        
        <div className="w-full max-w-lg">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            className="w-full rounded-md bg-gray-800 p-4 text-white placeholder-gray-400"
            disabled={isLoading}
          />
          <button
            onClick={handleScan}
            disabled={isLoading || !url.trim()}
            className="mt-4 w-full rounded-md bg-purple-600 p-4 font-bold text-white hover:bg-purple-500 disabled:bg-gray-500 disabled:cursor-not-allowed"
          >
            {isLoading ? "Scanning..." : "Scan Now"}
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="w-full max-w-2xl rounded-lg bg-red-900 p-4 text-red-200">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Loading State */}
        {isLoading && (
          <div className="text-gray-400">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-400 mx-auto"></div>
            <p className="mt-2">Scanning for vulnerabilities...</p>
          </div>
        )}

        {/* Results Section */}
        {results.length > 0 && (
          <div className="w-full max-w-2xl">
            <h2 className="text-2xl font-bold mb-4">Scan Results</h2>
            {results.map((result, index) => (
              <div key={index} className="mb-4 rounded-lg bg-gray-800 p-6">
                <h3 className="text-xl font-bold mb-2">{result.vulnerability}</h3>
                <div className="flex items-center mb-2">
                  <span className="font-semibold mr-2">Status:</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-bold ${
                    result.vulnerable 
                      ? 'bg-red-600 text-red-100' 
                      : 'bg-green-600 text-green-100'
                  }`}>
                    {result.vulnerable ? 'VULNERABLE' : 'SECURE'}
                  </span>
                </div>
                <p className="text-gray-300">{result.details}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
