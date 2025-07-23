from pydantic import BaseModel
from typing import List, Optional


class FileUpload(BaseModel):
    filename: str
    content: str


class MigrationRequest(BaseModel):
    files: List[FileUpload]


class MigrationResponse(BaseModel):
    success: bool
    plan_content: Optional[str] = None
    error: Optional[str] = None
    filename: str = "Plan.md"
