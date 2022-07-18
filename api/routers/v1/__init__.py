from fastapi import APIRouter

router = APIRouter(tags=["API Version 1"])

from api.routers.v1.endpoints import *
