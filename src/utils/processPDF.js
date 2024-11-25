import fs from "fs";
import pdfParse from "pdf-parse";
import path from "path";

export async function extractAbstractsFromFiles(files) {
  const abstracts = [];

  // Ambil teks abstrak dari setiap file PDF
  for (const filePath of files) {
    const fullPath = path.join(process.cwd(), "public", filePath);
    const fileBuffer = fs.readFileSync(fullPath);

    // Baca teks dari file PDF
    const pdfData = await pdfParse(fileBuffer);

    // Ekstrak abstrak
    const abstractText = extractAbstract(pdfData.text);

    // Tambahkan abstrak ke array
    abstracts.push({ file: filePath, abstract: abstractText });
  }

  console.log(abstracts);

  return abstracts;
}

// Fungsi untuk mengambil teks abstrak
function extractAbstract(text) {
  const abstractStart = /abstract|abstrak/i; // Kata kunci awal abstrak
  const abstractEnd = /kata kunci|keywords|introduction|background|chapter 1/i; // Kata kunci akhir abstrak

  const startMatch = text.match(abstractStart);
  const endMatch = text.match(abstractEnd);

  if (startMatch) {
    const startIndex = startMatch.index;
    const endIndex = endMatch ? endMatch.index : text.length;
    return text.slice(startIndex, endIndex).trim();
  }
  return "Abstract not found.";
}
