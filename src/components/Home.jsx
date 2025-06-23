"use client";

import React from "react";
import { useRouter } from "next/navigation";
import Navbar from "../components/Navbar";

const Home = () => {
  const router = useRouter();

  const handleGoToCompare = () => {
    router.push("/file-preview");
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <Navbar />
      <main className="flex flex-col items-center justify-center mt-20 text-center">
        <h2 className="text-3xl font-bold mb-4 text-red-600">
          Compare Your Journals
        </h2>
        <p className="text-gray-600 mb-8 max-w-lg">
          Upload and compare 2 journal files side-by-side to check their
          similarity score and AI-generated insights.
        </p>
        <button
          onClick={handleGoToCompare}
          className="bg-red-500 hover:bg-red-600 text-white py-3 px-6 rounded transition"
        >
          Go to Compare
        </button>
      </main>
    </div>
  );
};

export default Home;
