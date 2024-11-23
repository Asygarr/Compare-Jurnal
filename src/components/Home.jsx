"use client";

import React from "react";
import Navbar from "../components/Navbar";
import { useRouter } from "next/navigation";

const Home = () => {
  const router = useRouter();

  const handleFileChange = (e) => {
    const files = e.target.files;
    console.log(files);
    // Navigate to the file preview page
    router.push("/file-preview");
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <Navbar />
      <main className="flex flex-col items-center justify-center mt-13">
        <h2 className="text-3xl font-semibold mb-4 text-red-600 text-center">
          Compare Your Journals
        </h2>
        <p className="text-gray-600 mb-8 text-center">
          Upload multiple journal files to compare their content effectively.
        </p>
        <label
          htmlFor="file-upload"
          className="bg-red-500 hover:bg-red-600 text-white py-3 px-6 rounded cursor-pointer"
        >
          Select Files
        </label>
        <input
          id="file-upload"
          type="file"
          multiple
          className="hidden"
          onChange={handleFileChange}
        />
      </main>
    </div>
  );
};

export default Home;
