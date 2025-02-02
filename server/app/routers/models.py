from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from model.matcher import IssueMatcher
import json

router = APIRouter()

class FileInfo(BaseModel):
    name: str
    path: str
    download_url: str

class IssueDetails(BaseModel):
    owner: str
    repo: str
    title: str
    description: str = Field(..., description="Issue description with markdown formatting")
    labels: List[str]

class AnalyzeIssueRequest(BaseModel):
    owner: str
    repo: str
    filteredFiles: List[FileInfo]
    issueDetails: IssueDetails

@router.post("/analyse-issue")
async def analyze_issue(request: Request) -> Dict[str, Any]:
    try:
        # Get raw request body first
        raw_body = await request.body()
        body = json.loads(raw_body.decode("utf-8"))
        
        # Validate with Pydantic after parsing
        validated_request = AnalyzeIssueRequest(**body)
        
        matcher = IssueMatcher()
        
        # Run the matching
        result = await matcher.match_files(
            validated_request.issueDetails.dict(),
            [file.dict() for file in validated_request.filteredFiles]
        )
        
        return result
        
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid JSON format: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing issue: {str(e)}"
        )