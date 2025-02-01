from pydantic import BaseModel, HttpUrl
from typing import List

class FilteredFile(BaseModel):
    name: str
    path: str
    download_url: HttpUrl

class IssueDetails(BaseModel):
    owner: str
    repo: str
    title: str
    description: str
    labels: List[str]

class KeywordMatchRequest(BaseModel):
    owner: str
    repo: str
    filteredFiles: List[FilteredFile]
    issueDetails: IssueDetails


class FileMatch(BaseModel):
    file_name: str
    match_score: int
    download_url: HttpUrl

class KeywordMatchResponse(BaseModel):
    filename_matches: List[FileMatch]
