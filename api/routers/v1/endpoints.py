import base64

from celery.result import AsyncResult
from fastapi import HTTPException, Request, Response

from api.core.models import RatelimitsExceededError, RequestValidationError
from api.core.ratelimits import limiter
from api.core.utils import FakeResponse, clean_html
from api.routers.v1 import router
from api.routers.v1.models import (
    CourseHeroError,
    FileNotFoundError,
    SearchResponse,
    SearchResult,
    SearchSuggestionsResponse,
    TaskCreateResponse,
    TaskNotReadyError,
    TaskStatusResponse,
)
from common.api import get_document, get_search, get_search_suggestions
from common.utils import make_filename_safe
from worker.server import app
from worker.tasks import get_pdf


@router.post(
    "/tasks/create",
    summary="Create a new task to download a document.",
    response_model=TaskCreateResponse,
    responses={
        404: {
            "model": FileNotFoundError,
        },
        422: {
            "model": RequestValidationError,
        },
        429: {
            "model": RatelimitsExceededError,
        },
        500: {
            "model": CourseHeroError,
        },
    },
)
@limiter.limit("5/5minutes")
def task_create(request: Request, id: str):
    """
    Ratelimits: 5 requests per 5 minutes
    """
    doc_resp = get_document(id)
    if doc_resp.status_code == 404:
        raise HTTPException(
            status_code=404, detail="The file you're looking for doesn't exist."
        )
    if doc_resp.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong when contacting CourseHero.",
        )
    doc = doc_resp.json()
    task = get_pdf.delay(doc)
    return FakeResponse(TaskCreateResponse(task_id=task.id))


@router.get(
    "/tasks/{id}/status",
    summary="Get the status of a task.",
    response_model=TaskStatusResponse,
)
def task_status(id: str):
    res = AsyncResult(id, app=app)
    extra = res.info

    if res.state == "STARTED":
        return TaskStatusResponse(
            status=res.state,
            current_task=extra.get("current_task"),
        )
    return TaskStatusResponse(status=res.state)


@router.get(
    "/tasks/{id}/download",
    summary="Get the result of a task.",
    responses={
        200: {
            "content": {
                "application/pdf": {},
                "application/json": None,
            }
        },
        400: {"model": TaskNotReadyError},
    },
)
def task_get(id: str):
    res = AsyncResult(id, app=app)
    if not res.ready():
        raise HTTPException(
            status_code=400,
            detail="The given task doesn't exist or isn't ready. Please monitor the /status endpoint to see when your task is completed as tasks expire after 30 seconds.",
        )
    pdf, doc_name = res.get()
    resp = Response(base64.b64decode(pdf), media_type="application/pdf")
    resp.headers["Content-Disposition"] = f"attachment; filename={make_filename_safe(doc_name)}.pdf"
    resp.headers["Content-Type"] = "application/pdf"
    return resp


@router.get(
    "/search",
    summary="Search for a document.",
    response_model=SearchResponse,
    responses={
        200: {"model": SearchResponse},
        422: {
            "model": RequestValidationError,
        },
        429: {"model": RatelimitsExceededError},
        500: {"model": CourseHeroError},
    },
)
@limiter.limit("50/5minutes")
async def search(request: Request, query: str):
    """
    Ratelimits: 50 requests per 5 minutes
    """
    j = get_search(query)
    if j is None:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong when contacting CourseHero.",
        )

    return FakeResponse(
        SearchResponse(
            results=[
                SearchResult(
                    title=clean_html(r.get("core").get("title")),
                    document_id=r.get("document").get("db_filename"),
                    thumbnail=f"https://www.coursehero.com{r.get('thumbnail').get('url')}",
                    views=r.get("core").get("views"),
                    date=r.get("core").get("date"),
                )
                for r in j.get("results")
            ]
        )
    )


@router.get(
    "/suggestions",
    summary="Get search suggestions.",
    response_model=SearchSuggestionsResponse,
    responses={
        200: {
            "model": SearchSuggestionsResponse,
        },
        422: {
            "model": RequestValidationError,
        },
        500: {
            "model": CourseHeroError,
        },
    },
)
async def suggestions(request: Request, query: str):
    j = get_search_suggestions(query)
    if j is None:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong when contacting CourseHero.",
        )

    return SearchSuggestionsResponse(
        suggestions=[suggestion["suggestion"] for suggestion in j]
    )
