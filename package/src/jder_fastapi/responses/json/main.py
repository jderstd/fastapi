from typing import Any, Mapping, Optional, TypeVar

from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

T = TypeVar("T")


class JsonResponseError(BaseModel):
    """
    JSON response error.
    """

    code: str
    """
    Code representing the error.
    """
    path: list[str] = Field(default_factory=list)
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
    errors: list[JsonResponseError] = []
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

    errors: list[JsonResponseError] = []
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
    status: int = 200

    headers: Mapping[str, str] = {
        **(dict(response.headers) if response else {}),
        **(options.headers if options and options.headers else {}),
    }

    body: JsonResponse[T] | None = None

    # success
    if isinstance(options, CreateJsonSuccessResponseOptions):
        status = options.status if options and options.status else 200

        body = JsonResponse(
            success=True,
            data=options.data,
            errors=[],
        )

    # failure
    elif isinstance(options, CreateJsonFailureResponseOptions):
        status = options.status if options and options.status else 400

        body = JsonResponse(
            success=False,
            data=None,
            errors=options.errors,
        )

    # dataless success
    if body is None:
        body = JsonResponse(
            success=True,
            data=None,
            errors=[],
        )

    return JSONResponse(
        status_code=status,
        headers=headers,
        content=body.model_dump(),
    )
