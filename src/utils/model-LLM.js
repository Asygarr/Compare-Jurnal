import { InferenceClient } from "@huggingface/inference";

const client = new InferenceClient(process.env.HUGGINGFACE_API_KEY);

export async function generateCreativeResponseLLM(
  text1,
  text2,
  similarityScore,
  labelKemiripan
) {
  try {
    const messages = [
      {
        role: "system",
        content: "Anda adalah AI cerdas untuk perbandingan jurnal.",
      },
      {
        role: "user",
        content: `
            Saya akan memberikan dua abstrak jurnal beserta skor similarity yang telah dihitung menggunakan model sentence-transformers.
    
            Informasi:
            - Label Kemiripan: ${labelKemiripan}
            - Skor Kemiripan: ${similarityScore.toFixed(2)}
            - Abstrak 1: ${text1}
            - Abstrak 2: ${text2}
    
            Berdasarkan informasi tersebut, analisislah kedua jurnal dengan memberikan:
            1. Ringkasan dari masing-masing jurnal.
            2. Penjelasan mengenai kesamaan dan perbedaan utama.
            3. Analisis hubungan antara kedua jurnal.
            4. Kesimpulan apakah kedua jurnal sangat mirip atau memiliki perbedaan signifikan.
          `,
      },
    ];

    try {
      const response = await client.chatCompletion({
        provider: "hf-inference",
        model: "HuggingFaceH4/zephyr-7b-beta",
        messages: messages,
        // max_tokens: 512,
        temperature: 0.7,
      });

      return response.choices[0].message.content;
    } catch (error) {
      console.error("Terjadi kesalahan:", error);
    }
  } catch (error) {
    console.error("Error calling LLM:", error);
    throw new Error("Failed to generate creative response");
  }
}
