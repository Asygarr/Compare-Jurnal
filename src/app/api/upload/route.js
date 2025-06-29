import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function POST(req) {
  try {
    const data = await req.formData();
    const files = data.getAll("files");

    if (files.length > 2) {
      return NextResponse.json(
        { error: "Only up to 2 files are allowed." },
        { status: 400 }
      );
    }

    const uploadDir = path.join(process.cwd(), "public/uploads");
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }

    const fileInfos = [];

    for (const file of files) {
      const buffer = Buffer.from(await file.arrayBuffer());

      const sanitizedFileName = file.name.replace(/\s+/g, "_");
      const filePath = path.join(uploadDir, sanitizedFileName);

      fs.writeFileSync(filePath, buffer);
      fileInfos.push({
        name: sanitizedFileName,
        path: `/uploads/${sanitizedFileName}`,
      });
    }

    return NextResponse.json({ files: fileInfos });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
