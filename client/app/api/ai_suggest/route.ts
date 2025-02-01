import { NextResponse } from 'next/server';
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || '',
});

export async function POST(request: Request) {
  try {
    // Validate OpenAI API key
    if (!process.env.OPENAI_API_KEY) {
      return NextResponse.json(
        { error: 'OpenAI API key is not configured' },
        { status: 500 }
      );
    }

    // Parse the entire request body
    const fullData = await request.json();

    // Extract unique languages and topics
    const userLanguages = [...new Set(
      fullData.repositories
        .map((repo: any) => repo.language)
        .filter(Boolean)
    )];

    const userTopics = [...new Set(
      fullData.repositories
        .flatMap((repo: any) => repo.topics || [])
    )];

     // Filter out pull requests by checking if the issue has a pull_request property
     const availableIssues = fullData.repoissues.filter((issue: any) => !issue.pull_request);

     // If no valid issues are available, return early
     if (availableIssues.length === 0) {
       return NextResponse.json({
         reply: {
           recommendations: []
         }
       });
     }


    // Create a comprehensive prompt
   const prompt = `
OPEN-SOURCE CONTRIBUTION MATCHER

## DEVELOPER SKILLS
- Programming Languages: ${userLanguages.join(', ')}
- Technical Interests: ${userTopics.join(', ')}

## AVAILABLE ISSUES (Total: ${availableIssues.length})
${availableIssues.map((issue: any, index: number) => `
Issue #${index + 1}:
- Title: ${issue.title}
- Repository: ${fullData.issue_owner}/${fullData.issue_repo}
- Full GitHub Issue URL: https://github.com/${fullData.issue_owner}/${fullData.issue_repo}/issues/${issue.number}
`).join('\n')}

## RECOMMENDATION OBJECTIVE
Analyze the available issues and recommend ONLY those that match the developer's skills and interests.
Important constraints:
- Recommend a MAXIMUM of 3 issues
- Only recommend issues that genuinely match the developer's background
- If no issues match well, return an empty recommendations array
- Never recommend pull requests
- If there are fewer than 3 matching issues, only recommend those that truly fit

FORMAT YOUR RESPONSE AS JSON.
`;

    const completion = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        {
          role: "system",
          content: `You are an expert open-source contribution advisor. Only respond in valid JSON format. Your response must contain no more than 3 recommendations, and may contain 0 if no issues are suitable matches. Never include pull requests in recommendations.

          Response format:
          {
            "recommendations": [
              {
                "issue_title": "Exact Issue Title from Input",
                "issue_url": "https://github.com/{issue_owner}/{issue_repo}/issues/{issue_number}",
                "difficulty_level": "Beginner/Intermediate/Advanced",
                "learning_opportunities": "Specific skills to learn",
                "why_recommended": "Detailed explanation of why this issue is a good match"
              }
            ]
          }`
        },
        {
          role: "user",
          content: prompt
        }
      ],
      temperature: 0.7,
      max_tokens: 600
    });

    const recommendationContent = completion.choices[0]?.message?.content;

    if (!recommendationContent) {
      return NextResponse.json(
        { error: 'Failed to generate recommendations' },
        { status: 500 }
      );
    }

    const sanitizedContent = recommendationContent.replace(/```.*?(\n|$)/g, '').trim();

    try {
      const parsedRecommendations = JSON.parse(sanitizedContent);

      // Validate the response format and constraints
      if (!Array.isArray(parsedRecommendations.recommendations)) {
        throw new Error('Recommendations are not in the expected array format');
      }

      // Ensure we never exceed 3 recommendations
      parsedRecommendations.recommendations = parsedRecommendations.recommendations.slice(0, 3);

      return NextResponse.json({
        reply: { recommendations: parsedRecommendations.recommendations }
      });

    } catch (error) {
      console.error('AI Recommendation Error:', error, sanitizedContent);
      return NextResponse.json(
        {
          error: 'Issue recommendation process failed',
          details: error
        },
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