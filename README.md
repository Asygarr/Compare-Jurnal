# Journal Comparison System

This is a [Next.js](https://nextjs.org) project for academic journal comparison and analysis with AI-enhanced abstract extraction capabilities.

## Features

- **Smart Abstract Extraction**: Uses regex patterns for fast extraction, with Google Gemini AI as a fallback for complex journal formats
- **Journal Comparison**: Compare abstracts between different academic papers
- **Similarity Analysis**: Analyze similarity scores between journal abstracts
- **Multi-language Support**: Supports both Indonesian and English content

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Configuration

Copy the example environment file and add your API keys:

```bash
cp .env.example .env.local
```

Edit `.env.local` and add your Google Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

To get a Gemini API key:

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy it to your `.env.local` file

### 3. Run the Development Server

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## How Abstract Extraction Works

The system uses a two-tier approach for abstract extraction:

1. **Primary Method**: Fast regex-based extraction for standard journal formats
2. **Fallback Method**: Google Gemini AI extraction for non-standard or complex formats

When regex extraction fails or returns insufficient text (< 100 characters), the system automatically:

- Extracts the first 2000 words or 2 pages of the PDF
- Sends this text to Gemini AI with a specialized prompt
- Uses temperature 0.1 to minimize hallucination and ensure accuracy
- Returns the exact abstract text without modifications

## Project Structure

- `src/utils/process-pdf.js` - Enhanced PDF processing with AI fallback
- `src/utils/model-gemini.js` - Gemini AI integration
- `public/uploads/` - Uploaded PDF files
- `python/` - Python scripts for clustering and analysis

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
