import fs from "fs";
import pdfParse from "pdf-parse";
import path from "path";
import { GoogleGenAI } from "@google/genai";

// Initialize Gemini AI
const ai = new GoogleGenAI({
  apiKey: process.env.EXTRACT_API_KEY,
});

// Helper function to extract first 2000 words or 2 pages of text
function getInitialTextForAI(fullText) {
  const words = fullText.split(/\s+/);
  const first2000Words = words.slice(0, 2000).join(" ");

  // Alternatively, you could limit by characters (approximately 2 pages)
  const first2Pages = fullText.substring(0, 8000); // ~2 pages worth of text

  // Return the shorter of the two to be conservative
  return first2000Words.length < first2Pages.length
    ? first2000Words
    : first2Pages;
}

// Gemini AI abstract extraction function
async function extractAbstractWithAI(text) {
  const system = `You are a precise text extractor specialized in academic papers. Your ONLY task is to extract the abstract content paragraph.

    CRITICAL EXTRACTION RULES:
    1. Extract ONLY the main abstract paragraph content
    2. EXCLUDE headers like "ABSTRACT", "Abstract:", "Abstrak:", etc.
    3. EXCLUDE article metadata like "Article history:", "Received:", "Revised:", "Accepted:", etc.
    4. EXCLUDE keywords section
    5. Return the actual descriptive paragraph that explains the research
    6. Keep original punctuation and formatting exactly as written
    7. If no abstract content is found, return "ABSTRACT_NOT_FOUND"

    EXAMPLE:
    Input: "ABSTRACT\nArticle history:\nReceived Aug 18, 2023\n\nThis research aims to compare..."
    Output: "This research aims to compare..."`;

  const prompt = `Academic paper text to analyze:
    ${text}

    Extract ONLY the abstract content paragraph (exclude headers and metadata):`;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-2.0-flash",
      contents: prompt,
      config: {
        systemInstruction: system,
        temperature: 0.1,
        maxOutputTokens: 1000,
      },
    });

    let extractedText = response.text.trim();

    // Return null if AI couldn't find abstract
    if (extractedText === "ABSTRACT_NOT_FOUND" || extractedText.length < 50) {
      return null;
    }

    // Post-processing: Clean up any remaining headers or metadata
    extractedText = cleanExtractedAbstract(extractedText);

    return extractedText;
  } catch (error) {
    console.error("Error extracting abstract with AI:", error);
    return null;
  }
}

// Helper function to clean extracted abstract from any remaining headers/metadata
function cleanExtractedAbstract(text) {
  // Remove common headers and metadata patterns
  let cleanedText = text
    // Remove ABSTRACT headers
    .replace(/^(ABSTRACT|Abstract|Abstrak):?\s*/i, "")
    // Remove article history sections
    .replace(/Article\s+history:?\s*[\s\S]*?(?=\n\n|\n[A-Z])/i, "")
    // Remove received/revised/accepted lines
    .replace(/^(Received|Revised|Accepted|Published)[\s\S]*?\n/gim, "")
    // Remove date patterns (e.g., "Aug 18, 2023", "18 August 2023")
    .replace(
      /\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},?\s+\d{4}\b/gi,
      ""
    )
    // Remove standalone numbers and years at the beginning
    .replace(/^\d{1,2}\s+\w+\s+\d{4}\s*/gm, "")
    // Remove extra whitespace
    .replace(/\s+/g, " ")
    .trim();

  const metadataPattern =
    /^(Article\s+history|Received|Revised|Accepted|Keywords|DOI)/i;
  if (metadataPattern.test(cleanedText)) {
    // Find the first sentence that looks like abstract content (starts with capital letter and has research-related words)
    const sentences = cleanedText.split(/\.\s+/);
    for (let i = 0; i < sentences.length; i++) {
      const sentence = sentences[i].trim();
      if (
        sentence.length > 50 &&
        /^[A-Z]/.test(sentence) &&
        /(research|study|this|analysis|investigation|method|result)/i.test(
          sentence
        )
      ) {
        // Reconstruct from this sentence onwards
        cleanedText = sentences.slice(i).join(". ").trim();
        break;
      }
    }
  }

  return cleanedText;
}

export async function extractAbstractsFromFiles(files) {
  const abstractsDanKesimpulanSaran = [];

  for (const filePath of files) {
    const fullPath = path.join(process.cwd(), "public", filePath);
    const fileBuffer = fs.readFileSync(fullPath);

    const pdfData = await pdfParse(fileBuffer);
    const fileName = fullPath.split(path.sep).pop();
    const formattedFileName = fileName.replace(/_/g, " ");

    const initialText = getInitialTextForAI(pdfData.text);
    const abstractText = await extractAbstractWithAI(initialText);

    abstractsDanKesimpulanSaran.push({
      file: formattedFileName,
      abstract: abstractText,
    });
  }

  return abstractsDanKesimpulanSaran;
}
