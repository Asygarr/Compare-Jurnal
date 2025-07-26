import { NextResponse } from "next/server";
import { extractAbstractsFromFiles } from "@/utils/process-pdf";
import { getSimilarityFromPython } from "@/utils/call-ST";
import { generateCreativeResponseGemini } from "@/utils/model-gemini";

// test get path
export async function GET() {
  return NextResponse.json({ message: "Hello from the server!" });
}

export async function POST(request) {
  try {
    const { files } = await request.json();

    const extractAbstract = await extractAbstractsFromFiles(files);

    if (extractAbstract.length === 2) {
      const text1 = extractAbstract[0].abstract;
      const text2 = extractAbstract[1].abstract;

      if (text1 === null || text2 === null) {
        return NextResponse.json(
          {
            error:
              "Abstract not found. This may be due to the journal template not being supported yet.",
          },
          { status: 400 }
        );
      }

      const getSentenceTransformers = await getSimilarityFromPython(
        text1,
        text2
      );

      const roundedSimilarityScore = Math.round(
        getSentenceTransformers.similarity_score * 100
      );

      const creativeResponse = await generateCreativeResponseGemini(
        text1,
        text2,
        getSentenceTransformers.similarity_score,
        getSentenceTransformers.label_english
      );

      return NextResponse.json({
        success: true,
        similarity: {
          text1,
          text2,
          score: roundedSimilarityScore,
          label_kemiripan: getSentenceTransformers.label_kemiripan,
          label_english: getSentenceTransformers.label_english,
          bilingual_labels: getSentenceTransformers.bilingual_labels,
        },
        creativeResponse: {
          modelGenAI: creativeResponse,
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
