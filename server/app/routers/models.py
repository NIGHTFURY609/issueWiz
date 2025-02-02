from fastapi import APIRouter, HTTPException
from app.schemas.model_schemas import AnalyzeIssueRequest
from typing import List, Dict, Any
from model.matcher import IssueMatcher

router = APIRouter()

@router.post("/analyse-issue")
async def analyze_issue(request: AnalyzeIssueRequest) -> Dict[str, Any]:
    try:
        matcher = IssueMatcher()
        
        # Extract the issue details and filtered files
        issue_data = request.issueDetails.dict()
        filtered_files = [file.dict() for file in request.filteredFiles]
        
        # Run the matching
        result = await matcher.match_files(issue_data, filtered_files)
        
        # Return the raw result from the matcher
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing issue: {str(e)}"
        )