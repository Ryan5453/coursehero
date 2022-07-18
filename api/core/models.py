from pydantic import BaseModel, Field


class RequestValidationError(BaseModel):
    message: str = Field(
        ...,
        example="One or more parameters are invalid. Please check the documentation for more information.",
    )


class RatelimitsExceededError(BaseModel):
    message: str = Field(
        ...,
        example="You've exceeded your ratelimits. Please check the documentation for more information.",
    )
