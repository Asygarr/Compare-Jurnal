"use client";

import { useRouter } from "next/navigation";
import React, { useState } from "react";

const Navbar = () => {
  const route = useRouter();
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <header className="fixed top-0 left-0 w-full bg-white shadow-md py-5 px-10 flex justify-between items-center z-50">
      <div
        onClick={() => route.push("/home")}
        className="text-red-500 text-2xl font-bold cursor-pointer"
      >
        CompJurnal
      </div>
      <nav>
        <div className="md:hidden">
          <button
            onClick={toggleMenu}
            className="text-gray-700 focus:outline-none"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d={isOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16m-7 6h7"}
              ></path>
            </svg>
          </button>
        </div>
        <ul
          className={`md:flex space-x-6 text-gray-700 ${
            isOpen ? "block" : "hidden"
          } md:block`}
        >
          <li className="cursor-pointer">MERGE FILES</li>
          <li className="cursor-pointer">SPLIT FILES</li>
          <li className="cursor-pointer">COMPRESS FILES</li>
          <li className="cursor-pointer">COMPARE FILES</li>
          <li className="cursor-pointer">ALL TOOLS</li>
        </ul>
      </nav>
    </header>
  );
};

export default Navbar;
