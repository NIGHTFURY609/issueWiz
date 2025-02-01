from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.model_schemas import KeywordMatchRequest, KeywordMatchResponse
from model.matcher import IssueMatcher

router = APIRouter()

@router.post("/analyse-issue", response_model=KeywordMatchResponse)
async def process_request(request: KeywordMatchRequest):
    # Add machine learning code here to process the request and generate a response
    # For now, returning a basic response or raising an HTTPException
    try:
        issue_data = {
            "owner": request.owner,
            "repo": request.repo,
            "title": request.title,
            "description": request.description,
            "labels": request.labels
        }
        filtered_files = request.filteredFiles
        matcher = IssueMatcher()
        result = await matcher.match_files(issue_data, filtered_files)

        response = KeywordMatchResponse(filename_matches=result)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))