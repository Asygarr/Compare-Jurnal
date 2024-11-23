"use client";

import React, { useEffect, useState } from "react";
import Navbar from "../components/Navbar";

const FilePreview = () => {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    const storedFiles = localStorage.getItem("selectedFiles");
    if (storedFiles) {
      setFiles(JSON.parse(storedFiles));
    }
  }, []);

  const handleCompare = () => {
    console.log(
      "Files to compare:",
      files.map((file) => file.path)
    );
    alert("Compare button clicked. Check console for file paths.");
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <Navbar />
      <main className="flex flex-col items-center justify-center mt-13 w-full px-4">
        <h2 className="text-3xl font-semibold mb-4 text-red-600">
          File Preview
        </h2>
        <p className="text-gray-600 mb-8 text-center">
          Preview the content of your uploaded journal files.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl">
          {files.map((file, index) => (
            <div key={index} className="bg-white p-4 shadow rounded">
              <h3 className="font-semibold text-lg mb-2">{file.name}</h3>
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
      </main>
    </div>
  );
};

export default FilePreview;
