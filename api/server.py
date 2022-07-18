from fastapi import FastAPI

from api.routers.v1 import router as v1_router

description = """
This is the backend API that powers https://coursehero.app.

Please view the description of each endpoint in the documentation as some endpoints have ratelimits.

Please be respectful and do not abuse this API.
"""

app = FastAPI(docs_url="/", redoc_url=None, description=description, version="1.0.0")

app.include_router(v1_router, prefix="/v1")

from api.core.exceptions import *
