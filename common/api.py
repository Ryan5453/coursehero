from copy import copy
from typing import Optional

from common.constants import *


def get_document(id: str) -> Optional[dict]:
    return HTTP_CLIENT.get(
        f"{API_BASE_URL}/v1/documents/{id}",
        headers=API_HEADERS,
        params=API_BASE_PARAMS,
    )


def get_document_previews(id: str) -> Optional[dict]:
    return HTTP_CLIENT.get(
        f"{API_BASE_URL}/v1/documents/{id}/previewInfo",
        headers=API_HEADERS,
        params=API_BASE_PARAMS,
    )


def get_search(query: str) -> Optional[dict]:
    data = {
        "client": "ios",
        "client_id": API_CLIENT_ID,
        "client_secret": API_CLIENT_SECRET,
        "filters[type][]": ["document"],
        "limit": "20",
        "location[auto]": "1",
        "offset": "0",
        "query": query,
        "sort": "relevancy",
        "trigger": "ios_app",
        "view": "list_m",
    }
    response = HTTP_CLIENT.post(
        f"{API_BASE_URL}/v2/search/",
        headers=API_HEADERS,
        data=data,
    )
    if response.status_code == 200:
        return response.json()


def get_search_suggestions(query: str) -> Optional[dict]:
    params = copy(API_BASE_PARAMS)
    params["query"] = query
    response = HTTP_CLIENT.get(
        f"{API_BASE_URL}/v1/search/suggest",
        headers=API_HEADERS,
        params=params,
    )
    if response.status_code == 200:
        return response.json()
