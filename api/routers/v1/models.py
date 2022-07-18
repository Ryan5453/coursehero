from typing import Optional

from pydantic import BaseModel, Field


class TaskNotReadyError(BaseModel):
    message: str = Field(
        example="The given task doesn't exist or isn't ready. Please monitor the /status endpoint to see when your task is completed."
    )


class TaskStatusResponse(BaseModel):
    status: str = Field(..., description="The status of the task.", example="PENDING")
    current_task: Optional[str] = Field(
        None, description="What is currently being processed.", example="Creating PDF"
    )


class TaskCreateResponse(BaseModel):
    task_id: str = Field(
        ...,
        description="The task's unique identifier.",
        example="2546ec81-6941-4566-bb63-421dfe840296",
    )


class FileNotFoundError(BaseModel):
    message: str = Field(..., example="The file you're looking for doesn't exist.")


class CourseHeroError(BaseModel):
    message: str = Field(
        ...,
        example="Something went wrong when contacting CourseHero.",
    )


class SearchResult(BaseModel):
    title: str = Field(
        ..., description="The title of the document.", example="AP Biology HW 1.docx"
    )
    document_id: int = Field(
        description="The document's unique identifier.", example=122971637
    )
    thumbnail: str = Field(
        description="A URL to the document's thumbnail.",
        example="https://www.coursehero.com/thumb/cf/78/cf78e52eaf380c112bec8ac3500d8b1c4305e49c_180.jpg",
    )
    views: int = Field(description="The number of views the document has.", example=0)
    date: str = Field(
        description="The date the document was uploaded.", example="2021-12-15"
    )


class SearchResponse(BaseModel):
    results: list[SearchResult]


class SearchSuggestionsResponse(BaseModel):
    suggestions: list[str] = Field(
        ..., example=["AP Biology Homework", "AP Chemistry Homework"]
    )
