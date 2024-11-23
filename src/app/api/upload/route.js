import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function POST(req) {
  try {
    const data = await req.formData();
    const files = data.getAll("files");

    const uploadDir = path.join(process.cwd(), "public/uploads");
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }

    const fileInfos = [];

    for (const file of files) {
      const buffer = Buffer.from(await file.arrayBuffer());
      const filePath = path.join(uploadDir, file.name);

      fs.writeFileSync(filePath, buffer);
      fileInfos.push({ name: file.name, path: `/uploads/${file.name}` });
    }

    return NextResponse.json({ files: fileInfos });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
