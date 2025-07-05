"use client";

import { useState, useEffect } from "react";
import { marked } from "marked";

export default function BilingualResultBox({ resultData }) {
  const [htmlContent, setHtmlContent] = useState("");
  const [currentLanguage, setCurrentLanguage] = useState("indonesian");
  const [isClient, setIsClient] = useState(false);

  // Ensure we're on the client side before accessing localStorage
  useEffect(() => {
    setIsClient(true);
    if (typeof window !== "undefined") {
      const savedLanguage =
        localStorage.getItem("preferredLanguage") || "indonesian";
      setCurrentLanguage(savedLanguage);
    }
  }, []);

  // Debug logging
  useEffect(() => {
    console.log("BilingualResultBox - resultData:", resultData);
    console.log("BilingualResultBox - typeof resultData:", typeof resultData);
    console.log("BilingualResultBox - currentLanguage:", currentLanguage);
  }, [resultData, currentLanguage]);

  // Update HTML content when language or data changes
  useEffect(() => {
    if (resultData && resultData[currentLanguage]) {
      console.log(
        `Content for ${currentLanguage}:`,
        resultData[currentLanguage]
      );

      const html = marked.parse(resultData[currentLanguage]);
      setHtmlContent(html);
    }
  }, [resultData, currentLanguage]);

  // Handle language toggle
  const toggleLanguage = (language) => {
    setCurrentLanguage(language);
    if (typeof window !== "undefined") {
      localStorage.setItem("preferredLanguage", language);
    }
  };

  // Handle case where resultData is a string (backward compatibility)
  if (typeof resultData === "string") {
    console.log("Displaying string data as fallback");

    // Try to parse if it looks like JSON
    try {
      const parsedData = JSON.parse(resultData);
      if (parsedData.indonesian || parsedData.english) {
        console.log("String contained JSON, parsing and re-rendering");
        return <BilingualResultBox resultData={parsedData} />;
      }
    } catch (e) {
      // Not JSON, treat as plain text
      console.log("String is not JSON, treating as plain text");
    }

    return (
      <div className="mt-4 space-y-4">
        <div className="p-4 bg-gray-100 border rounded text-gray-700 prose max-w-none">
          <div dangerouslySetInnerHTML={{ __html: marked.parse(resultData) }} />
        </div>
      </div>
    );
  }

  // Debug: Check if we're getting the raw JSON object
  if (
    resultData &&
    typeof resultData === "object" &&
    !resultData.indonesian &&
    !resultData.english
  ) {
    console.log("Raw result data:", resultData);
    return (
      <div className="mt-4 space-y-4">
        <div className="p-4 bg-yellow-100 border border-yellow-400 rounded text-yellow-700">
          <strong>Debug:</strong> Received object data but not in expected
          format. Check console for details.
        </div>
      </div>
    );
  }

  // Handle case where resultData doesn't have both languages
  if (!resultData || (!resultData.indonesian && !resultData.english)) {
    return (
      <div className="mt-4 space-y-4">
        <div className="p-4 bg-red-100 border border-red-400 rounded text-red-700">
          No bilingual content available. Please try again.
        </div>
      </div>
    );
  }

  // Don't render until we're on the client side
  if (!isClient) {
    return (
      <div className="mt-4 space-y-4">
        <div className="p-4 bg-gray-100 border rounded text-gray-700">
          Loading...
        </div>
      </div>
    );
  }

  return (
    <div className="mt-4 space-y-4">
      {/* Language Toggle Buttons */}
      <div className="flex gap-2 mb-4">
        <button
          onClick={() => toggleLanguage("indonesian")}
          className={`px-4 py-2 rounded font-medium transition-colors ${
            currentLanguage === "indonesian"
              ? "bg-red-600 text-white"
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"
          }`}
          disabled={!resultData.indonesian}
        >
          🇮🇩 Bahasa Indonesia
        </button>
        <button
          onClick={() => toggleLanguage("english")}
          className={`px-4 py-2 rounded font-medium transition-colors ${
            currentLanguage === "english"
              ? "bg-red-600 text-white"
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"
          }`}
          disabled={!resultData.english}
        >
          🇺🇸 English
        </button>
      </div>

      {/* Content Display */}
      <div className="p-6 bg-white border rounded-lg shadow-sm text-gray-800 prose prose-lg max-w-none">
        {htmlContent ? (
          <div
            className="formatted-content"
            dangerouslySetInnerHTML={{ __html: htmlContent }}
          />
        ) : (
          <div className="text-gray-500 italic">
            Content not available in{" "}
            {currentLanguage === "indonesian" ? "Indonesian" : "English"}.
          </div>
        )}
      </div>

      {/* Language Indicator */}
      <div className="text-sm text-gray-500 text-right">
        Currently showing:{" "}
        {currentLanguage === "indonesian" ? "Bahasa Indonesia" : "English"}
      </div>
    </div>
  );
}
