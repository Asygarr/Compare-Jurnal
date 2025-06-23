"use client";

import { useState, useEffect } from "react";
import { marked } from "marked";

export default function ResultBox({ resultText }) {
  const [htmlContent, setHtmlContent] = useState("");

  useEffect(() => {
    if (resultText) {
      const html = marked.parse(resultText);
      setHtmlContent(html);
    }
  }, [resultText]);

  return (
    <div className="mt-4 space-y-4">
      <div className="p-4 bg-gray-100 border rounded text-gray-700 prose max-w-none">
        <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
      </div>
    </div>
  );
}
