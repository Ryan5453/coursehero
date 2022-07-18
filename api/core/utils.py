import regex
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

HTML_REGEX = regex.compile("<.*?>")


def clean_html(text):
    return HTML_REGEX.sub("", text)


def FakeResponse(model: BaseModel):
    return JSONResponse(
        content=jsonable_encoder(model),
    )
