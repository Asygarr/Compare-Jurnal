"use client";

import React, { useEffect, useState } from "react";
import Navbar from "../components/Navbar";

const FilePreview = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <Navbar />
      <main className="flex flex-col items-center justify-center mt-13">
        <h2 className="text-3xl font-semibold mb-4 text-red-600">
          File Preview
        </h2>
        <p className="text-gray-600 mb-8 text-center">
          Here you can preview the content of your uploaded journal files.
        </p>
        {/* Add preview Logic Here */}
      </main>
    </div>
  );
};

export default FilePreview;
