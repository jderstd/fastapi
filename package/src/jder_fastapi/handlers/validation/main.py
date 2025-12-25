from typing import Sequence

from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, TypeAdapter

from jder_fastapi.responses.error import ResponseError
from jder_fastapi.responses.json import (
    CreateJsonFailureResponseOptions,
    JsonResponseError,
    createJsonResponse,
)


class Error(BaseModel):
    model_config = ConfigDict(extra="ignore")
    type: str | None
    loc: list[str] | None
    msg: str | None


Errors = TypeAdapter(Sequence[Error])


def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    A custom exception handler for `RequestValidationError`.

    ### Example

    ```python
    from fastapi import FastAPI
    from fastapi.requests import Request
    from fastapi.responses import JSONResponse
    from fastapi.exceptions import RequestValidationError
    from jder_fastapi.handlers import request_validation_exception_handler

    app: FastAPI = FastAPI()


    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        req: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return request_validation_exception_handler(req, exc)
    ```
    """
    errs: Sequence[Error] = Errors.validate_python(exc.errors())

    status: int = 400

    code: str = ResponseError.PARSE.to_code()

    if len(errs) == 0:
        return createJsonResponse(
            options=CreateJsonFailureResponseOptions(
                status=status,
                errors=[
                    JsonResponseError(
                        code=code,
                    )
                ],
            )
        )

    errors: list[JsonResponseError] = []

    for err in errs:
        errors.append(
            JsonResponseError(
                code=code,
                path=err.loc if err.loc is not None else [],
                message=err.msg,
            )
        )

    return createJsonResponse(
        options=CreateJsonFailureResponseOptions(
            status=status,
            errors=errors,
        )
    )
