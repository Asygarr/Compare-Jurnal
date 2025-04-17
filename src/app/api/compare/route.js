import { NextResponse } from "next/server";
import { extractAbstractsFromFiles } from "@/utils/process-pdf";
import { getSimilarityFromPython } from "@/utils/call-ST";
import { generateCreativeResponseGemini } from "@/utils/model-gemini";
import { generateCreativeResponseLLM } from "@/utils/model-LLM";

// test get path
export async function GET() {
  return NextResponse.json({ message: "Hello from the server!" });
}

export async function POST(request) {
  try {
    const { files } = await request.json();

    const abstractsDanSaran = await extractAbstractsFromFiles(files);

    if (abstractsDanSaran.length === 2) {
      const text1 = abstractsDanSaran[0].abstract;
      const text2 = abstractsDanSaran[1].abstract;

      const getSentenceTransformers = await getSimilarityFromPython(
        text1,
        text2
      );
      const similarityPercentage = (
        getSentenceTransformers.similarity_score * 100
      ).toFixed(2);

      // const creativeResponse1 = await generateCreativeResponseLLM(
      //   text1,
      //   text2,
      //   getSentenceTransformers
      // );
      const creativeResponse2 = await generateCreativeResponseGemini(
        text1,
        text2,
        getSentenceTransformers.similarity_score
      );

      // const creativeResponse =
      //   creativeResponse1 || creativeResponse2 || "No response generated.";

      const creativeResponse = creativeResponse2;

      return NextResponse.json({
        success: true,
        // abstractsDanSaran,
        similarity: {
          text1,
          text2,
          score: similarityPercentage,
          label_kemiripan: getSentenceTransformers.label_kemiripan,
        },
        creativeResponse: {
          modelGPT: creativeResponse,
        },
      });
    } else {
      return NextResponse.json(
        { error: "At least two abstracts are required for comparison" },
        { status: 400 }
      );
    }
  } catch (error) {
    console.error("Error processing files:", error);
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    );
  }
}
