from typing import Any, Mapping, Optional, TypeVar

from fastapi.responses import Response
from pydantic import BaseModel

T = TypeVar("T")


class CreateResponseOptions[T = Any](BaseModel):
    """
    Options of `createResponse` function.
    """

    status: Optional[int] = None
    """
    Status code of the response.
    """
    headers: Optional[Mapping[str, str]] = None
    """
    Headers of the response.
    """
    body: Optional[T] = None
    """
    Body of the response.
    """


def createResponse(
    response: Response | None = None,
    options: CreateResponseOptions[T] | None = None,
) -> Response:
    """
    Create a response.

    ### Example

    ```python
    from fastapi import FastAPI
    from fastapi.responses import Response
    from jder_fastapi.responses import createResponse

    app: FastAPI = FastAPI()


    @app.get("/")
    async def route() -> Response:
        return createResponse(
            {
                "headers": {
                    "Content-Type": "text/plain",
                },
                "body": "Hello, World!",
            },
        )
    ```
    """
    status: int = 200
    headers: Mapping[str, str] = {}
    body: T | None = None

    if response:
        headers = dict(response.headers or {})

    if options:
        if options.status:
            status = options.status
        if options.headers:
            headers = {**headers, **options.headers}
        if options.body:
            body = options.body

    return Response(
        status_code=status,
        headers=headers,
        content=body,
    )
