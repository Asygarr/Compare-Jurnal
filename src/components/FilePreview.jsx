"use client";

import React, { useEffect, useState } from "react";
import { formatMarkdownResponse } from "@/utils/markedTeks";
import Navbar from "../components/Navbar";

const FilePreview = () => {
  const [files, setFiles] = useState([]);
  const [comparisonResult, setComparisonResult] = useState(null); // Untuk menyimpan hasil

  useEffect(() => {
    const storedFiles = localStorage.getItem("selectedFiles");
    if (storedFiles) {
      setFiles(JSON.parse(storedFiles));
    }
  }, []);

  const handleCompare = async () => {
    try {
      const response = await fetch("/api/compare", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ files: files.map((file) => file.path) }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();
      setComparisonResult(result);
    } catch (error) {
      console.error("Error comparing files:", error.message);
      setComparisonResult(["Error processing comparison."]);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <Navbar />
      <main className="flex flex-col items-center justify-center w-full overflow-y-auto min-h-screen pt-24 pb-10">
        <h2 className="text-3xl font-semibold mb-4 text-red-600">
          File Preview
        </h2>
        <p className="text-gray-600 mb-8 text-center">
          Preview the content of your uploaded journal files.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl">
          {files.map((file, index) => (
            <div key={index} className="bg-white p-4 shadow rounded">
              <h3 className="font-semibold text-lg mb-2 text-red-600">
                {file.name}
              </h3>
              <iframe
                src={file.path}
                className="w-full h-64 border"
                title={file.name}
              />
            </div>
          ))}
        </div>
        <button
          onClick={handleCompare}
          className="mt-8 bg-red-600 text-white py-2 px-6 rounded hover:bg-red-700"
        >
          Compare
        </button>

        {/* Tampilkan hasil di sini */}
        {comparisonResult && (
          <div className="mt-8 w-full max-w-4xl bg-white p-6 shadow rounded">
            <h3 className="font-semibold text-lg text-red-600 mb-4">
              Comparison Results
            </h3>
            <div className="space-y-4">
              <div className="p-4 bg-gray-100 border rounded text-gray-700">
                <div
                  className="whitespace-pre-wrap"
                  dangerouslySetInnerHTML={formatMarkdownResponse(
                    comparisonResult.creativeResponse.modelGPT
                  )}
                />
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default FilePreview;
