const { GoogleGenerativeAI } = require("@google/generative-ai");

const genAI = new GoogleGenerativeAI(process.env.GPT_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

export async function generateCreativeResponse(text1, text2, similarityScore) {
  //   const prompt2 = `
  //         Berikut adalah dua abstrak dari jurnal dan skor kemiripan mereka:
  //         1. Abstrak Pertama: ${text1}
  //         2. Abstrak Kedua: ${text2}
  //         Skor Kemiripan: ${similarityScore.toFixed(2)}

  //         Berdasarkan informasi di atas, buatlah sebuah respons kreatif yang menjelaskan:
  //         - Ringkasan Jurnal berdasarkan dari kedua Abstrak.
  //         - Hubungan Antara Jurnal dari kedua abstrak.
  //         - Kemiripan Jurnal, apakah abstrak ini sangat mirip atau berbeda berdasarkan skor similarity (Tanpa menyebutkan score similarity pada response).

  //         Tulis jawaban dalam bahasa indonesia yang jelas, ringkas, dan mudah dipahami.
  //       `;

  const prompt = {
    task: "Comparing Journals from Journal Abstracts",
    language: "bahasa indonesia",
    data: `
            Abstrak pertama: ${text1}
            Abstrak kedua: ${text2}
            Skor similarity: ${similarityScore.toFixed(2)}
          `,
    notes: `
            Berdasarkan informasi data di atas, buatlah sebuah respons kreatif yang menjelaskan:
            - Ringkasan Jurnal berdasarkan dari kedua Abstrak.
            - Hubungan Antara Jurnal dari kedua abstrak.
            - Kemiripan Jurnal, apakah abstrak ini sangat mirip atau berbeda berdasarkan skor similarity (Tanpa menyebutkan score similarity pada response).
          `,
  };

  try {
    const result = await model.generateContent(JSON.stringify(prompt));
    return result.response.text();
  } catch (error) {
    console.error("Error calling GPT:", error);
    throw new Error("Failed to generate creative response");
  }
}
