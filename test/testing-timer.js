// ⏱️ SIMPLE TIMER + CSV EXPORT
console.log("🚀 Starting Performance Test with CSV Export...\n");

const fs = require("fs");
const fetch = (...args) =>
  import("node-fetch").then(({ default: fetch }) => fetch(...args));

const testCases = [
  {
    files: [
      "file-test/Cukup Berkaitan/CB-1.pdf",
      "file-test/Cukup Berkaitan/CB-2.pdf",
    ],
    label: "Test 1 - Cukup Berkaitan",
  },
  {
    files: [
      "file-test/Sangat Berkaitan/SB-1.pdf",
      "file-test/Sangat Berkaitan/SB-2.pdf",
    ],
    label: "Test 2 - Sangat Berkaitan",
  },
  {
    files: [
      "file-test/Sedikit Berkaitan/SeB-1.pdf",
      "file-test/Sedikit Berkaitan/SeB-2.pdf",
    ],
    label: "Test 3 - Sedikit Berkaitan",
  },
  {
    files: [
      "file-test/Tidak Relevan/TR-1.pdf",
      "file-test/Tidak Relevan/TR-2.pdf",
    ],
    label: "Test 4 - Tidak Relevan",
  },
];

async function singleTest(files, label) {
  console.log(`⏱️ ${label}: Testing...`);

  const start = Date.now();

  try {
    const response = await fetch("http://localhost:3000/api/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ files }),
    });

    const end = Date.now();
    const timeSeconds = (end - start) / 1000;

    if (response.ok) {
      const data = await response.json();
      console.log(
        `✅ ${label}: ${timeSeconds.toFixed(2)}s - Similarity: ${
          data.similarity?.score
        }%`
      );
      return {
        time: timeSeconds,
        similarity: data.similarity?.score,
        success: true,
      };
    } else {
      const error = await response.json();
      console.log(
        `❌ ${label}: ${timeSeconds.toFixed(2)}s - Error: ${error.error}`
      );
      return { time: timeSeconds, similarity: null, success: false };
    }
  } catch (error) {
    console.log(`❌ ${label}: Error - ${error.message}`);
    return null;
  }
}

async function runTestAndExport() {
  const results = [];
  const csvData = ["Test,Response Time (seconds),Similarity (%),Status"];

  for (let i = 0; i < testCases.length; i++) {
    const testCase = testCases[i];
    const result = await singleTest(testCase.files, testCase.label);

    if (result !== null) {
      results.push(result);
      csvData.push(
        `${testCase.label},${result.time.toFixed(2)},${
          result.similarity || "N/A"
        },${result.success ? "Success" : "Failed"}`
      );
    }

    if (i < testCases.length - 1) {
      console.log("   Waiting 2 seconds...\n");
      await new Promise((resolve) => setTimeout(resolve, 2000));
    }
  }

  // Calculate results
  const successfulResults = results.filter((r) => r.success);

  console.log("\n📊 RESULTS SUMMARY:");
  console.log("=".repeat(80));

  // Display results in table format
  console.log("\n📋 DETAILED RESULTS TABLE:");
  console.log(
    "┌─────────────────────────────┬──────────────┬─────────────┬──────────┐"
  );
  console.log(
    "│ Test Category               │ Time (sec)   │ Similarity  │ Status   │"
  );
  console.log(
    "├─────────────────────────────┼──────────────┼─────────────┼──────────┤"
  );

  results.forEach((result, index) => {
    const category = testCases[index].label.split(" - ")[1] || "Unknown";
    const time = result.time.toFixed(2).padEnd(12);
    const similarity = (
      result.similarity ? result.similarity + "%" : "N/A"
    ).padEnd(11);
    const status = (result.success ? "✅ Success" : "❌ Failed").padEnd(8);
    console.log(
      `│ ${category.padEnd(27)} │ ${time} │ ${similarity} │ ${status} │`
    );
  });

  console.log(
    "└─────────────────────────────┴──────────────┴─────────────┴──────────┘"
  );

  if (successfulResults.length > 0) {
    const times = successfulResults.map((r) => r.time);
    const averageTime =
      times.reduce((sum, time) => sum + time, 0) / times.length;
    const minTime = Math.min(...times);
    const maxTime = Math.max(...times);

    console.log("\n📈 STATISTICAL SUMMARY:");
    console.log("┌─────────────────────────────┬──────────────┐");
    console.log("│ Metric                      │ Value        │");
    console.log("├─────────────────────────────┼──────────────┤");
    console.log(
      `│ Successful Tests            │ ${successfulResults.length}/${testCases.length}          │`
    );
    console.log(
      `│ Average Response Time       │ ${averageTime.toFixed(2)}s       │`
    );
    console.log(
      `│ Fastest Response            │ ${minTime.toFixed(2)}s       │`
    );
    console.log(
      `│ Slowest Response            │ ${maxTime.toFixed(2)}s       │`
    );
    console.log("└─────────────────────────────┴──────────────┘");

    // Add summary to CSV
    csvData.push("");
    csvData.push("SUMMARY");
    csvData.push(`Average,${averageTime.toFixed(2)},N/A,N/A`);
    csvData.push(`Fastest,${minTime.toFixed(2)},N/A,N/A`);
    csvData.push(`Slowest,${maxTime.toFixed(2)},N/A,N/A`);

    console.log(`\n🎯 CONCLUSION FOR SKRIPSI:`);
    console.log(
      "┌─────────────────────────────────────────────────────────────────────────┐"
    );
    console.log(
      "│                           HASIL PENGUJIAN                              │"
    );
    console.log(
      "├─────────────────────────────────────────────────────────────────────────┤"
    );
    console.log(
      `│ Rata-rata waktu respons sistem: ${averageTime.toFixed(
        2
      )} detik                      │`
    );
    console.log(
      "│ Pengujian dilakukan pada 4 kategori kemiripan jurnal                   │"
    );
    console.log(
      "│ dengan metode blackbox testing                                          │"
    );
    console.log(
      "└─────────────────────────────────────────────────────────────────────────┘"
    );
  } else {
    console.log("\n❌ TIDAK ADA TEST YANG BERHASIL");
    console.log(
      "┌─────────────────────────────────────────────────────────────────────────┐"
    );
    console.log(
      "│ Semua test gagal. Periksa koneksi server dan file test.                │"
    );
    console.log(
      "└─────────────────────────────────────────────────────────────────────────┘"
    );
  }

  // Export to CSV pada direktori test
  const csvFilePath = "test/performance_results.csv";
  fs.writeFileSync(csvFilePath, csvData.join("\n"), "utf8");
  console.log(`\n📂 Hasil pengujian diekspor ke ${csvFilePath}`);
  console.log("✅ Pengujian selesai!");
}

runTestAndExport();
