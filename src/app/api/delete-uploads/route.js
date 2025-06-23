import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function POST() {
  const dir = path.join(process.cwd(), "public/uploads");
  fs.readdirSync(dir).forEach((file) => {
    fs.unlinkSync(path.join(dir, file));
  });
  return NextResponse.json({ message: "Files deleted." });
}
