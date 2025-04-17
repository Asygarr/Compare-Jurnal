export async function getSimilarityFromPython(text1, text2) {
  try {
    const response = await fetch("http://127.0.0.1:8000/similarity/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text1, text2 }),
    });

    if (!response.ok) {
      throw new Error(`Error from Python backend: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error calling Python backend:", error);
    throw error;
  }
}
