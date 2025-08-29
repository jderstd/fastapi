from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.requests import Request
from fastapi.responses import Response
from jder_fastapi.handlers import (
    request_validation_exception_handler,
)
from jder_fastapi.responses.json import (
    CreateJsonFailureResponseOptions,
    CreateJsonSuccessResponseOptions,
    JsonResponse,
    JsonResponseError,
    createJsonResponse,
)
from pydantic import BaseModel

app: FastAPI = FastAPI()


@app.get("/", response_model=JsonResponse)
async def route_index() -> Response:
    return createJsonResponse()


class Info(BaseModel):
    name: str
    version: str


@app.get("/info", response_model=JsonResponse[Info])
async def route_info(res: Response) -> Response:
    res.headers["X-Test"] = "test"
    return createJsonResponse(
        res,
        CreateJsonSuccessResponseOptions(
            data=Info(
                name="example",
                version="0.1.0",
            )
        ),
    )


class Item(BaseModel):
    id: int


@app.get("/items/{item_id}", response_model=JsonResponse[Item])
async def route_validate(item_id: int, res: Response) -> Response:
    return createJsonResponse(
        res,
        CreateJsonSuccessResponseOptions(data=Item(id=item_id)),
    )


@app.exception_handler(404)
async def http_404_handler(req: Request, exc: HTTPException) -> Response:
    return createJsonResponse(
        options=CreateJsonFailureResponseOptions(
            status=exc.status_code,
            headers=exc.headers or {},
            errors=[
                JsonResponseError(
                    code="not_found",
                )
            ],
        )
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    req: Request, exc: RequestValidationError
) -> Response:
    return request_validation_exception_handler(req, exc)
