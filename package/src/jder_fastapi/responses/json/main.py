from typing import Any, Mapping, Optional, TypeVar

from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

T = TypeVar("T")


class JsonResponseError(BaseModel):
    """
    JSON response error.
    """

    code: str
    """
    Code representing the error.
    """
    path: Optional[list[str]] = None
    """
    Indicates where the error occurred.
    """
    message: Optional[str] = None
    """
    Detail of the error.
    """


class JsonResponse[T = Any](BaseModel):
    """
    JSON response.
    """

    success: bool
    """
    Indicates whether the response is successful or not.
    """
    data: Optional[T] = None
    """
    Requested information for the response when `success` is `true`.
    """
    errors: Optional[list[JsonResponseError]] = None
    """
    A list of errors for the response when `success` is `false`.
    """


class CreateJsonResponseBaseOptions(BaseModel):
    """
    Base options of `createJsonResponse` function.
    """

    status: Optional[int] = None
    """
    Status code of the response.
    By default, it is `200` for success and `400` for failure.
    """
    headers: Optional[Mapping[str, str]] = None
    """
    Additional headers of the response.
    """


class CreateJsonSuccessResponseOptions[T = Any](CreateJsonResponseBaseOptions):
    """
    Options of `createJsonResponse` function.
    """

    data: Optional[T] = None
    """
    Requested information for the response when `success` is `true`.
    """


class CreateJsonFailureResponseOptions(CreateJsonResponseBaseOptions):
    """
    Options of `createJsonResponse` function.
    """

    errors: Optional[list[JsonResponseError]] = None
    """
    A list of errors for the response when `success` is `false`.
    """


def createJsonResponse(
    response: Response | None = None,
    options: CreateJsonSuccessResponseOptions[T]
    | CreateJsonFailureResponseOptions
    | None = None,
) -> JSONResponse:
    """
    Create a JSON response.

    ### Examples

    Example for creating a successful JSON response without data:

    ```python
    from fastapi import FastAPI
    from fastapi.responses import Response
    from jder_fastapi.responses.json import createJsonResponse

    app: FastAPI = FastAPI()


    @app.get("/")
    async def route() -> Response:
        return createJsonResponse()
    ```

    Example for creating a successful JSON response with data:

    ```python
    from fastapi import FastAPI
    from fastapi.responses import Response
    from jder_fastapi.responses.json import createJsonResponse

    app: FastAPI = FastAPI()


    @app.get("/")
    async def route() -> Response:
        return createJsonResponse(
            options={
                "data": "Hello, World!",
            }
        )
    ```

    Example for creating a failure JSON response:

    ```python
    from fastapi import FastAPI
    from fastapi.responses import Response
    from jder_fastapi.responses.json import createJsonResponse

    app: FastAPI = FastAPI()


    @app.get("/")
    async def route() -> Response:
        return createJsonResponse(
            options={
                "status": 500,
                "errors": [
                    {
                        "code": "server",
                        "message": "Internal server error",
                    },
                ],
            }
        )
    ```

    Example for merging response:

    ```python
    from fastapi import FastAPI
    from fastapi.responses import Response
    from jder_fastapi.responses.json import createJsonResponse

    app: FastAPI = FastAPI()


    @app.get("/")
    async def route(res: Response) -> Response:
        return createJsonResponse(res)
    ```
    """
    is_failure: bool = isinstance(options, CreateJsonFailureResponseOptions)

    status: int = (
        options.status
        if options and options.status
        else (400 if is_failure else 200)
    )

    headers: Mapping[str, str] = {
        **(dict(response.headers) if response else {}),
        **(options.headers if options and options.headers else {}),
    }

    body: JsonResponse[T] = JsonResponse(
        success=not is_failure,
        data=options.data
        if isinstance(options, CreateJsonSuccessResponseOptions)
        else None,
        errors=options.errors if is_failure else None,
    )

    return JSONResponse(
        status_code=status,
        headers=headers,
        content=body.model_dump(exclude_none=True),
    )
