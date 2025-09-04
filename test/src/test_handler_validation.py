from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import Response as FastApiResponse
from fastapi.testclient import TestClient
from httpx import Response as HttpxResponse
from jder_fastapi.handlers import request_validation_exception_handler
from jder_fastapi.responses.error import ResponseError
from jder_fastapi.responses.json import (
    CreateJsonSuccessResponseOptions,
    JsonResponse,
    createJsonResponse,
)
from pydantic import BaseModel

app: FastAPI = FastAPI()


class Data(BaseModel):
    id: int


@app.get("/items/{id}")
async def index(id: int) -> FastApiResponse:
    return createJsonResponse(
        options=CreateJsonSuccessResponseOptions(data=Data(id=id))
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> FastApiResponse:
    return request_validation_exception_handler(request, exc)


client: TestClient = TestClient(app)


def test_success():
    res: HttpxResponse = client.get("/items/1")
    assert res.status_code == 200

    json: JsonResponse[Data] = JsonResponse[Data].model_validate(res.json())

    assert json.success == True

    assert json.data is not None

    assert json.data.id == 1


def test_failure():
    res: HttpxResponse = client.get("/items/abc")
    assert res.status_code == 400

    json: JsonResponse[Data] = JsonResponse[Data].model_validate(res.json())

    assert json.success == False

    assert json.errors is not None

    assert json.errors[0].code == ResponseError.PARSE.to_code()
    assert json.errors[0].path == ["path", "id"]
    assert (
        json.errors[0].message
        == "Input should be a valid integer, unable to parse string as an integer"
    )
