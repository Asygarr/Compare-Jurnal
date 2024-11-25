import { NextResponse } from "next/server";
import { extractAbstractsFromFiles } from "@/utils/processPDF";

// test get path
export async function GET() {
  return NextResponse.json({ message: "Hello from the server!" });
}

export async function POST(request) {
  try {
    const { files } = await request.json(); // Path file yang dikirim dari frontend

    // memanggil fungsi extractAbstractsFromFiles
    const abstracts = await extractAbstractsFromFiles(files);

    return NextResponse.json({ success: true, abstracts });
  } catch (error) {
    console.error("Error processing files:", error);
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    );
  }
}
