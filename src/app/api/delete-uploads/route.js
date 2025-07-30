import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function POST() {
  try {
    const dir = path.join(process.cwd(), "public/uploads");

    // Check if directory exists
    if (!fs.existsSync(dir)) {
      return NextResponse.json({
        message: "Upload directory not found, nothing to delete.",
      });
    }

    // Read directory contents
    const items = fs.readdirSync(dir);

    let deletedCount = 0;

    for (const item of items) {
      const itemPath = path.join(dir, item);
      const stat = fs.statSync(itemPath);

      if (stat.isFile()) {
        // Delete files only
        fs.unlinkSync(itemPath);
        deletedCount++;
      } else if (stat.isDirectory()) {
        // Recursively delete directories and their contents
        fs.rmSync(itemPath, { recursive: true, force: true });
        deletedCount++;
      }
    }

    return NextResponse.json({
      message: `Successfully deleted ${deletedCount} item(s).`,
      deletedCount,
    });
  } catch (error) {
    return NextResponse.json(
      {
        error: "Failed to delete files",
        details: error.message,
      },
      { status: 500 }
    );
  }
}
