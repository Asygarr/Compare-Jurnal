import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({
  apiKey: process.env.GEMINI_API_KEY,
});

export async function generateCreativeResponseGemini(
  text1,
  text2,
  similarityScore,
  labelKemiripan
) {
  const system =
    "You are an AI for journal comparison. Analyze the two journal abstracts and provide a comprehensive comparison in both Indonesian and English.";

  const content = `
    Similarity Label: ${labelKemiripan}
    Similarity Score: ${similarityScore}
    Abstract 1: ${text1}
    Abstract 2: ${text2}

    Analyze and compare these journals.`;

  // Define the response schema
  const responseSchema = {
    type: "object",
    properties: {
      indonesian: {
        type: "object",
        properties: {
          title: { type: "string" },
          firstJournalSummary: { type: "string" },
          secondJournalSummary: { type: "string" },
          similarities: {
            type: "array",
            items: { type: "string" },
          },
          differences: {
            type: "array",
            items: { type: "string" },
          },
          relationshipAnalysis: { type: "string" },
          conclusion: { type: "string" },
        },
        required: [
          "title",
          "firstJournalSummary",
          "secondJournalSummary",
          "similarities",
          "differences",
          "relationshipAnalysis",
          "conclusion",
        ],
      },
      english: {
        type: "object",
        properties: {
          title: { type: "string" },
          firstJournalSummary: { type: "string" },
          secondJournalSummary: { type: "string" },
          similarities: {
            type: "array",
            items: { type: "string" },
          },
          differences: {
            type: "array",
            items: { type: "string" },
          },
          relationshipAnalysis: { type: "string" },
          conclusion: { type: "string" },
        },
        required: [
          "title",
          "firstJournalSummary",
          "secondJournalSummary",
          "similarities",
          "differences",
          "relationshipAnalysis",
          "conclusion",
        ],
      },
    },
    required: ["indonesian", "english"],
  };

  try {
    const response = await ai.models.generateContent({
      model: "gemini-2.0-flash",
      contents: content,
      config: {
        systemInstruction: system,
        temperature: 0.7,
        maxOutputTokens: 1500,
        responseMimeType: "application/json",
        responseSchema: responseSchema,
      },
    });

    const responseText = response.text;
    const parsedResponse = JSON.parse(responseText);

    // Format the response into markdown
    const formattedResponse = {
      indonesian: formatToMarkdown(parsedResponse.indonesian, "indonesian"),
      english: formatToMarkdown(parsedResponse.english, "english"),
    };

    return formattedResponse;
  } catch (error) {
    console.error("Error calling Gemini:", error);
    throw new Error("Failed to generate creative response");
  }
}

function formatToMarkdown(data, language) {
  const translations = {
    indonesian: {
      firstJournalTitle: "## 1. Ringkasan Jurnal Pertama",
      secondJournalTitle: "## 2. Ringkasan Jurnal Kedua",
      similaritiesTitle: "## Kesamaan Utama:",
      differencesTitle: "## Perbedaan Utama:",
      analysisTitle: "## Analisis Hubungan",
      conclusionTitle: "## Kesimpulan",
    },
    english: {
      firstJournalTitle: "## 1. First Journal Summary",
      secondJournalTitle: "## 2. Second Journal Summary",
      similaritiesTitle: "## Main Similarities:",
      differencesTitle: "## Main Differences:",
      analysisTitle: "## Relationship Analysis",
      conclusionTitle: "## Conclusion",
    },
  };

  const t = translations[language];

  let markdown = `# ${data.title}\n\n`;
  markdown += `${t.firstJournalTitle}\n${data.firstJournalSummary}\n\n`;
  markdown += `${t.secondJournalTitle}\n${data.secondJournalSummary}\n\n`;

  markdown += `${t.similaritiesTitle}\n`;
  data.similarities.forEach((similarity) => {
    markdown += `- ${similarity}\n`;
  });
  markdown += `\n`;

  markdown += `${t.differencesTitle}\n`;
  data.differences.forEach((difference) => {
    markdown += `- ${difference}\n`;
  });
  markdown += `\n`;

  markdown += `${t.analysisTitle}\n${data.relationshipAnalysis}\n\n`;
  markdown += `${t.conclusionTitle}\n${data.conclusion}`;

  return markdown;
}
