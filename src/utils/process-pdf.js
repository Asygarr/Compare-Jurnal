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
  const system = `You are a precise text extractor specialized in academic papers. Extract the abstract content from academic papers.`;

  const content = `Academic paper text: ${text}
    Extract the abstract content in English. If no English abstract is found, extract the abstract in Indonesian. Return only the main abstract paragraph without headers or metadata.`;

  // Define the response schema
  const responseSchema = {
    type: "object",
    properties: {
      abstractContent: {
        type: "string",
        description:
          "The extracted abstract content without headers or metadata",
      },
      isFound: {
        type: "boolean",
        description: "Whether an abstract was successfully found and extracted",
      },
    },
    required: ["abstractContent", "isFound"],
  };

  try {
    const response = await ai.models.generateContent({
      model: "gemini-2.0-flash",
      contents: content,
      config: {
        systemInstruction: system,
        temperature: 0.1,
        maxOutputTokens: 1000,
        responseMimeType: "application/json",
        responseSchema: responseSchema,
      },
    });

    const responseText = response.text;
    const parsedResponse = JSON.parse(responseText);

    // Return null if AI couldn't find abstract
    if (!parsedResponse.isFound || parsedResponse.abstractContent.length < 50) {
      return null;
    }

    return parsedResponse.abstractContent;
  } catch (error) {
    console.error("Error extracting abstract with AI:", error);
    return null;
  }
}

export async function extractAbstractsFromFiles(files) {
  const abstractJournal = [];

  for (const filePath of files) {
    const fullPath = path.join(process.cwd(), "public", filePath);
    const fileBuffer = fs.readFileSync(fullPath);

    const pdfData = await pdfParse(fileBuffer);
    const fileName = fullPath.split(path.sep).pop();
    const formattedFileName = fileName.replace(/_/g, " ");

    const initialText = getInitialTextForAI(pdfData.text);
    const abstractText = await extractAbstractWithAI(initialText);

    abstractJournal.push({
      file: formattedFileName,
      abstract: abstractText,
    });
  }

  return abstractJournal;
}
