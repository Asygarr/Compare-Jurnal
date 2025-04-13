import fs from "fs";
import pdfParse from "pdf-parse";
import path from "path";

export async function extractAbstractsFromFiles(files) {
  const abstractsDanKesimpulanSaran = [];

  for (const filePath of files) {
    const fullPath = path.join(process.cwd(), "public", filePath);
    const fileBuffer = fs.readFileSync(fullPath);

    const pdfData = await pdfParse(fileBuffer);
    const fileName = fullPath.split(path.sep).pop();
    const formattedFileName = fileName.replace(/_/g, " ");

    const abstractText = extractAbstract(pdfData.text);
    const kesimpulanSaranText = extractKesimpulan(pdfData.text);

    abstractsDanKesimpulanSaran.push({
      file: formattedFileName,
      abstract: abstractText,
      kesimpulanDanSaran: kesimpulanSaranText,
    });
  }

  return abstractsDanKesimpulanSaran;
}

function extractAbstract(text) {
  const abstractStart = /abstrak|intisari/i;
  const abstractEnd = /kata kunci|introduction|background|chapter 1/i;

  const startMatch = text.match(abstractStart);
  const endMatch = text.match(abstractEnd);

  if (startMatch) {
    const startIndex = startMatch.index;
    const endIndex = endMatch ? endMatch.index : text.length;
    return text.slice(startIndex, endIndex).trim();
  }
  return "Abstract not found.";
}

function extractKesimpulan(text) {
  const kesimpulanSaranStart = /kesimpulan/gi;
  const kesimpulanSaranEnd =
    /daftar pustaka|referensi|ucapan terima kasih|references/i;

  // Cari semua kemunculan "kesimpulan"
  const allMatches = [...text.matchAll(kesimpulanSaranStart)];
  if (allMatches.length === 0) {
    return "Kesimpulan dan Saran not found.";
  }

  // Ambil "kesimpulan" terakhir
  const startMatch = allMatches[allMatches.length - 1];
  const startIndex = startMatch.index;

  // Cari batas akhir dari section
  const endMatch = text.slice(startIndex).match(kesimpulanSaranEnd);
  const endIndex = endMatch ? startIndex + endMatch.index : text.length;

  return text.slice(startIndex, endIndex).trim();
}

function extractSaran(text) {
  const kesimpulanSaranStart = /saran/gi;
  const kesimpulanSaranEnd =
    /daftar pustaka|referensi|ucapan terima kasih|references/i;

  // Cari semua kemunculan "kesimpulan"
  const allMatches = [...text.matchAll(kesimpulanSaranStart)];
  if (allMatches.length === 0) {
    return 0;
  }

  // Ambil "kesimpulan" terakhir
  const startMatch = allMatches[allMatches.length - 1];
  const startIndex = startMatch.index;

  // Cari batas akhir dari section
  const endMatch = text.slice(startIndex).match(kesimpulanSaranEnd);
  const endIndex = endMatch ? startIndex + endMatch.index : text.length;

  return text.slice(startIndex, endIndex).trim();
}
