"use client";

import React, { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import BilingualResultBox from "@/components/BilingualResultBox";
import BilingualSimilarityBox from "@/components/BilingualSimilarityBox";
import LanguageToggle from "@/components/LanguageToggle";

const FilePreview = () => {
  const [files, setFiles] = useState([]);
  const [comparisonResult, setComparisonResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [popupMessage, setPopupMessage] = useState("");
  const [popupType, setPopupType] = useState("");

  // Load existing uploaded files on mount
  useEffect(() => {
    const storedFiles = JSON.parse(localStorage.getItem("selectedFiles")) || [];
    setFiles(storedFiles);
  }, []);

  // Show popup message
  const showPopup = (message, type = "info") => {
    setPopupMessage(message);
    setPopupType(type);
    setTimeout(() => {
      setPopupMessage("");
    }, 2000);
  };

  // Upload handler
  const handleFileUpload = async (e) => {
    const newFiles = e.target.files;
    if (files.length + newFiles.length > 2) {
      showPopup("You can only upload 2 files for comparison.", "error");
      return;
    }

    const formData = new FormData();
    Array.from(newFiles).forEach((file) => formData.append("files", file));

    const response = await fetch("/api/upload", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    if (response.ok) {
      const updatedFiles = [...files, ...result.files];
      localStorage.setItem("selectedFiles", JSON.stringify(updatedFiles));
      setFiles(updatedFiles);
      showPopup(
        `${result.files.length} file(s) uploaded successfully.`,
        "success"
      );
    } else {
      showPopup(result.error || "Upload failed.", "error");
    }

    e.target.value = null;
  };

  // Compare handler
  const handleCompare = async () => {
    setIsLoading(true);
    setComparisonResult(null);

    try {
      const response = await fetch("/api/compare", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ files: files.map((file) => file.path) }),
      });

      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Comparison failed.");
      setComparisonResult(result);
      showPopup("Comparison complete!", "success");
    } catch (error) {
      // console.error("Compare Error:", error);
      showPopup(error.message || "Comparison failed.", "error");
    } finally {
      setIsLoading(false);
    }
  };

  // Reset handler (hapus localStorage & file uploads di server)
  const handleResetUpload = async () => {
    await fetch("/api/delete-uploads", { method: "POST" });
    localStorage.removeItem("selectedFiles");
    setFiles([]);
    setComparisonResult(null);
    showPopup("Uploads reset successfully.", "success");
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <Navbar />
      <main className="flex flex-col items-center justify-center w-full overflow-y-auto min-h-screen pt-24 pb-10">
        <h2 className="text-3xl font-bold mb-4 text-red-600">File Preview</h2>
        <p className="text-gray-600 mb-8 text-center">
          Upload up to 2 journal files for comparison.
        </p>

        {/* Upload / Compare Button */}
        {files.length < 2 ? (
          <label className="bg-red-500 hover:bg-red-600 text-white py-2 px-6 rounded cursor-pointer">
            Upload File
            <input type="file" onChange={handleFileUpload} className="hidden" />
          </label>
        ) : (
          <button
            onClick={handleCompare}
            className="bg-red-600 text-white py-2 px-6 rounded hover:bg-red-700"
          >
            {isLoading ? "Comparing..." : "Compare"}
          </button>
        )}

        {/* Reset Button */}
        {files.length > 0 && (
          <button
            onClick={handleResetUpload}
            className="mt-4 bg-gray-400 hover:bg-gray-500 text-white py-2 px-6 rounded"
          >
            Reset Upload
          </button>
        )}

        {/* Uploaded File Preview */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl mt-10">
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

        {/* Comparison Result */}
        {comparisonResult && !isLoading && (
          <div className="mt-10 w-full max-w-4xl bg-white p-6 shadow rounded">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-semibold text-lg text-red-600">
                Comparison Results
              </h3>
              {/* Language Toggle */}
              <LanguageToggle />
            </div>

            {/* Bilingual Similarity Display */}
            <BilingualSimilarityBox
              similarityData={comparisonResult.similarity}
            />

            {/* Creative Response */}
            <BilingualResultBox
              resultData={comparisonResult.creativeResponse.modelGenAI}
            />
          </div>
        )}
      </main>

      {/* Pop Up Message */}
      {popupMessage && (
        <div
          className={`fixed top-5 right-5 px-4 py-2 rounded shadow-lg z-50 text-white animate-fade-in ${
            popupType === "success"
              ? "bg-green-500"
              : popupType === "error"
              ? "bg-red-500"
              : "bg-blue-500"
          }`}
        >
          {popupMessage}
        </div>
      )}

      {/* Animasi CSS */}
      <style jsx>{`
        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fade-in {
          animation: fade-in 0.3s ease-out;
        }
      `}</style>
    </div>
  );
};

export default FilePreview;
