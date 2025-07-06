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
    "You are an intelligent AI for journal comparison based on the information provided. Generate creative responses for journal analysis in both Indonesian and English languages. CRITICAL: You must respond ONLY with valid JSON format with 'indonesian' and 'english' keys. Do not include any text before or after the JSON. Format the content with proper markdown structure including headers, bullet points, and paragraphs for better readability.";

  const content = `
      I will provide two journal abstracts along with a similarity score calculated using a sentence-transformers model. Here's how to interpret the similarity score:
      Information: 
      - Similarity Label: ${labelKemiripan}
      - Similarity Score: ${similarityScore.toFixed(2)}
      - Abstract 1: ${text1}
      - Abstract 2: ${text2}

      Based on this information, analyze both journals and provide ONLY a valid JSON response with this exact structure:
      {
        "indonesian": "# Ringkasan Perbandingan Jurnal\\n\\n## 1. Ringkasan Jurnal Pertama\\n• [summary points]\\n\\n## 2. Ringkasan Jurnal Kedua\\n• [summary points]\\n\\n## Kesamaan Utama:\\n- [similarity points]\\n\\n## Perbedaan Utama:\\n- [difference points]\\n\\n## Analisis Hubungan\\n[detailed analysis paragraphs]\\n\\n## Kesimpulan\\n[conclusion paragraph]",
        "english": "# Journal Comparison Summary\\n\\n## 1. First Journal Summary\\n• [summary points]\\n\\n## 2. Second Journal Summary\\n• [summary points]\\n\\n## Main Similarities:\\n- [similarity points]\\n\\n## Main Differences:\\n- [difference points]\\n\\n## Relationship Analysis\\n[detailed analysis paragraphs]\\n\\n## Conclusion\\n[conclusion paragraph]"
      }

      CRITICAL REQUIREMENTS:
      1. Respond ONLY with valid JSON - no additional text before or after
      2. Use markdown formatting with proper escape sequences for newlines (\\n\\n for paragraph breaks)
      3. Both language versions must be well-structured and complete
      4. Do not use any backticks or code block formatting in your response
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-2.0-flash",
      contents: content,
      config: {
        systemInstruction: system,
        temperature: 0.7,
        maxOutputTokens: 1500,
      },
    });

    const responseText = response.text;

    try {
      const parsedResponse = JSON.parse(responseText);

      if (parsedResponse.indonesian && parsedResponse.english) {
        return parsedResponse;
      }
    } catch (parseError) {
      let cleanedText = responseText.trim();

      if (cleanedText.startsWith("```json")) {
        cleanedText = cleanedText
          .replace(/^```json\s*/, "")
          .replace(/\s*```$/, "");
      } else if (cleanedText.startsWith("```")) {
        cleanedText = cleanedText.replace(/^```\s*/, "").replace(/\s*```$/, "");
      }

      const jsonMatch = cleanedText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        try {
          const extractedJson = JSON.parse(jsonMatch[0]);

          if (extractedJson.indonesian && extractedJson.english) {
            console.log("Successfully extracted both languages");
            return extractedJson;
          }
        } catch (extractError) {
          console.warn(
            "Could not parse extracted JSON, falling back to default structure:",
            extractError.message
          );
        }
      }

      console.log("Using fallback structure");
      return {
        indonesian: responseText,
        english: "English translation not available. Please try again.",
      };
    }

    return {
      indonesian: responseText,
      english: "English translation not available. Please try again.",
    };
  } catch (error) {
    console.error("Error calling Gemini:", error);
    throw new Error("Failed to generate creative response");
  }
}
