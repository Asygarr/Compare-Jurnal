"use client";

import { useState, useEffect } from "react";

export default function BilingualSimilarityBox({ similarityData }) {
  const [currentLanguage, setCurrentLanguage] = useState("english");
  const [isClient, setIsClient] = useState(false);

  // Ensure we're on the client side before accessing localStorage
  useEffect(() => {
    setIsClient(true);
    if (typeof window !== "undefined") {
      const savedLanguage = localStorage.getItem("preferredLanguage");
      if (
        savedLanguage &&
        (savedLanguage === "indonesian" || savedLanguage === "english")
      ) {
        setCurrentLanguage(savedLanguage);
      } else {
        // Set default to English and save it
        localStorage.setItem("preferredLanguage", "english");
        setCurrentLanguage("english");
      }
    }
  }, []);

  // Listen for language changes from other components
  useEffect(() => {
    const handleLanguageChange = (event) => {
      setCurrentLanguage(event.detail.language);
    };

    if (isClient) {
      window.addEventListener("languageChanged", handleLanguageChange);
      return () => {
        window.removeEventListener("languageChanged", handleLanguageChange);
      };
    }
  }, [isClient]);

  // Don't render until we're on the client side
  if (!isClient) {
    return <div>Loading...</div>;
  }

  // Handle case where similarityData is not available
  if (!similarityData || !similarityData.bilingual_labels) {
    return (
      <div className="p-4 bg-gray-100 border rounded-lg">
        <p className="text-gray-500">Similarity data not available</p>
      </div>
    );
  }

  const currentData = similarityData.bilingual_labels[currentLanguage];
  const scoreLabel = currentData?.scoreLabel || "Similarity Score";
  const similarityLabel =
    currentData?.similarity || similarityData.label_kemiripan;

  return (
    <div className="mt-4 space-y-4">
      {/* Similarity Metrics Display */}
      <div className="p-6 bg-white border rounded-lg shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Similarity Score */}
          <div className="text-center">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              {scoreLabel}
            </h3>
            <div className="text-3xl font-bold text-blue-600">
              {similarityData.score.toFixed(2)}%
            </div>
          </div>

          {/* Similarity Label */}
          <div className="text-center">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              {currentLanguage === "indonesian"
                ? "Label Kemiripan"
                : "Similarity Label"}
            </h3>
            <div className="text-xl font-medium text-green-600 bg-green-50 px-4 py-2 rounded-lg">
              {similarityLabel}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
