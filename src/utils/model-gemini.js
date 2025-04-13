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
    "Anda adalah AI cerdas untuk perbandingan jurnal berdasarkan dari informasi yang diberikan. jangan ada kalimat tanggapan, langsung pada proses untuk menghasilkan response creative dari hasil analisis informasi.";

  const content = `
      Saya akan memberikan dua abstrak jurnal beserta skor similarity yang telah dihitung menggunakan model sentence-transformers. Berikut cara interpretasi skor similarity:
      Informasi : 
      - Label Kemiripan : ${labelKemiripan}
      - Score Kemiripan : ${similarityScore.toFixed(2)}
      - Abstract 1 : ${text1}
      - Abstract 2 : ${text2}

      Berdasarkan informasi tersebut, analisislah kedua jurnal dengan memberikan:
      1. Ringkasan dari masing-masing jurnal.
      2. Penjelasan mengenai kesamaan dan perbedaan utama.
      3. Analisis hubungan antara kedua jurnal.
      4. Kesimpulan apakah kedua jurnal sangat mirip atau memiliki perbedaan signifikan.
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-2.0-flash",
      contents: content,
      config: {
        systemInstruction: system,
        temperature: 0.7,
        maxOutputTokens: 500,
      },
    });

    return response.text;
  } catch (error) {
    console.error("Error calling GPT:", error);
    throw new Error("Failed to generate creative response");
  }
}
