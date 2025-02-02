from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List,Dict
from model.matcher import IssueMatcher
import json
from app.schemas.model_schemas import KeywordMatchRequest, KeywordMatchResponse

router = APIRouter()

@router.post("/analyze_issue", response_model=KeywordMatchResponse)
async def analyze_issue(request: KeywordMatchRequest):
    matcher = IssueMatcher()
    try:
        # Extract issue data
        issue_data = {
            "owner": request.issueDetails.owner,
            "repo": request.issueDetails.repo,
            "title": request.issueDetails.title,
            "description": request.issueDetails.description,
            "labels": request.issueDetails.labels
        }
        
        # Convert filtered files to list of dicts
        filtered_files = [
            {
                "name": file.name,
                "path": file.path,
                "download_url": str(file.download_url)
            } 
            for file in request.filteredFiles
        ]
        result = await matcher.match_files(issue_data,filtered_files)
        result = json.dumps(result, indent=4)
        return KeywordMatchResponse(filename_matches=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))