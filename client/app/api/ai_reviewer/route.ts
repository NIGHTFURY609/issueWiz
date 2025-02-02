import { NextResponse } from 'next/server';
import OpenAI from 'openai';

// Initialize OpenAI client with API key
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || '',
});

// Constants for limiting analysis scope
const MAX_CHARS_PER_FILE = 1000; // Limit characters per file
const MAX_FILES = 3; // Limit number of files to analyze

// Helper function to fetch and truncate file content
async function fetchFileContent(url: string) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch file: ${response.statusText}`);
    }
    const content = await response.text();
    // Truncate content if too long, focusing on the beginning of the file
    return content.length > MAX_CHARS_PER_FILE 
      ? content.slice(0, MAX_CHARS_PER_FILE) + '\n... (content truncated)'
      : content;
  } catch (error) {
    console.error(`Error fetching file content: ${error}`);
    return null;
  }
}

// Interface defining the expected structure of the FastAPI response
interface FastAPIResponse {
  elapsed_time: number;
  matches: {
    filename_matches: Array<{
      file_name: string;
      match_score: number;
      download_url: string;
    }>;
  };
  status: string;
  message: string;
}

export async function POST(request: Request) {
  try {
    // Verify API key exists
    if (!process.env.OPENAI_API_KEY) {
      return NextResponse.json(
        { error: 'OpenAI API key is not configured' },
        { status: 500 }
      );
    }

    // Extract request data
    const requestData = await request.json();
    const { owner, repo, issue_title, issue_body } = requestData;

    // Extract filename matches from the nested structure
    // Note: We're now expecting the matches to be in the format returned by FastAPI
    const filename_matches = requestData.matchedFiles?.matches?.filename_matches;

    // Validate the matches array
    if (!Array.isArray(filename_matches)) {
      return NextResponse.json(
        { error: 'Invalid input: filename_matches is not available or not an array' },
        { status: 400 }
      );
    }

    // Sort and limit the number of files to analyze
    const topMatches = filename_matches
      .sort((a, b) => b.match_score - a.match_score)
      .slice(0, MAX_FILES);

    // Fetch truncated content of top matching files
    const fileContents = await Promise.all(
      topMatches.map(async (file) => ({
        file_name: file.file_name,
        match_score: file.match_score,
        content: await fetchFileContent(file.download_url)
      }))
    );

    // Filter out any null contents from failed fetches
    const validFileContents = fileContents.filter(file => file.content !== null);

    // Construct the analysis prompt
    const prompt = `
Analyze this GitHub issue and relevant files:

Repository: ${owner}/${repo}
Issue Title: ${issue_title}
Issue Description: ${issue_body?.slice(0, 500)}${issue_body?.length > 500 ? '... (truncated)' : ''}

Relevant Files:
${validFileContents.map(file => `
File: ${file.file_name}
Match Score: ${file.match_score}
Key Content:
${file.content}
`).join('\n')}

Provide analysis focusing on:
1. Repository purpose and tech stack
2. File relevance to issue
3. Specific recommendations for changes
`;

    // Make OpenAI API call
    const completion = await openai.chat.completions.create({
      model: "gpt-3.5-turbo-16k", // Using 16k context model for larger content
      messages: [
        {
          role: "system",
          content: `You are an expert code analyst and issue resolver. Respond in valid JSON format following this structure:
          {
            "repository_analysis": {
              "purpose": "Main purpose of the repository",
              "tech_stack": ["List", "of", "technologies"],
              "issue_summary": "Core problem analysis"
            },
            "file_analysis": {
              "analyzed_files": [
                {
                  "file_name": "path/to/file",
                  "combined_probability": number,
                  "reason": "Why this file needs modification"
                }
              ]
            },
            "recommendations": {
              "priority_order": ["Ordered", "list", "of", "files"],
              "specific_changes": "Detailed description of recommended changes",
              "additional_context": "Extra information needed"
            }
          }`
        },
        {
          role: "user",
          content: prompt
        }
      ],
      temperature: 0.7,
      max_tokens: 2000
    });

    // Extract and process the analysis content
    const analysisContent = completion.choices[0]?.message?.content;

    if (!analysisContent) {
      return NextResponse.json(
        { error: 'Failed to generate analysis' },
        { status: 500 }
      );
    }

    // Clean up the response and parse JSON
    const sanitizedContent = analysisContent.replace(/```.*?(\n|$)/g, '').trim();
    
    try {
      const parsedAnalysis = JSON.parse(sanitizedContent);
      return NextResponse.json({ reply: parsedAnalysis });
    } catch (error) {
      console.error('AI Analysis Error:', error, sanitizedContent);
      return NextResponse.json(
        { error: 'Issue analysis process failed', details: error },
        { status: 500 }
      );
    }

  } catch (error) {
    console.error('Error during POST request:', error);
    return NextResponse.json(
      { error: 'Internal Server Error', details: error },
      { status: 500 }
    );
  }
}