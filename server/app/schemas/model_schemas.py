from pydantic import BaseModel, HttpUrl
from typing import List


class FileInfo(BaseModel):
    name: str
    path: str
    download_url: str

class IssueDetails(BaseModel):
    owner: str
    repo: str
    title: str
    description: str
    labels: List[str]

class AnalyzeIssueRequest(BaseModel):
    owner: str
    repo: str
    filteredFiles: List[FileInfo]
    issueDetails: IssueDetails