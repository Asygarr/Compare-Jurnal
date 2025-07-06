"use client";

import { useState, useEffect } from "react";

export default function LanguageToggle() {
  const [currentLanguage, setCurrentLanguage] = useState("english");
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
    if (typeof window !== "undefined") {
      const savedLanguage =
        localStorage.getItem("preferredLanguage") || "english";
      setCurrentLanguage(savedLanguage);
    }
  }, []);

  useEffect(() => {
    if (isClient && typeof window !== "undefined") {
      localStorage.setItem("preferredLanguage", currentLanguage);

      window.dispatchEvent(
        new CustomEvent("languageChanged", {
          detail: { language: currentLanguage },
        })
      );
    }
  }, [currentLanguage, isClient]);

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

  const toggleLanguage = (language) => {
    setCurrentLanguage(language);
  };

  if (!isClient) {
    return null;
  }

  return (
    <div className="flex gap-2">
      <button
        onClick={() => toggleLanguage("english")}
        className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
          currentLanguage === "english"
            ? "bg-red-600 text-white"
            : "bg-gray-200 text-gray-700 hover:bg-gray-300"
        }`}
        title="English"
      >
        🇺🇸 EN
      </button>
      <button
        onClick={() => toggleLanguage("indonesian")}
        className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
          currentLanguage === "indonesian"
            ? "bg-red-600 text-white"
            : "bg-gray-200 text-gray-700 hover:bg-gray-300"
        }`}
        title="Bahasa Indonesia"
      >
        🇮🇩 ID
      </button>
    </div>
  );
}
