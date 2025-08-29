from typing import Any

from fastapi import FastAPI
from fastapi.responses import Response as FastApiResponse
from fastapi.testclient import TestClient
from httpx import Response as HttpxResponse
from jder_fastapi.responses.json import (
    CreateJsonFailureResponseOptions,
    JsonResponse,
    JsonResponseError,
    createJsonResponse,
)

app: FastAPI = FastAPI()


@app.get("/")
async def index() -> FastApiResponse:
    return createJsonResponse()


@app.get("/fail")
async def fail(res: FastApiResponse) -> FastApiResponse:
    return createJsonResponse(
        res,
        CreateJsonFailureResponseOptions(
            errors=[
                JsonResponseError(
                    code="parse",
                    path=["response"],
                    message="response error",
                )
            ]
        ),
    )


@app.get("/server")
async def server(res: FastApiResponse) -> FastApiResponse:
    return createJsonResponse(
        res,
        CreateJsonFailureResponseOptions(
            status=500,
            errors=[
                JsonResponseError(
                    code="server",
                    path=["server"],
                    message="server",
                )
            ],
        ),
    )


@app.get("/header")
async def header(res: FastApiResponse) -> FastApiResponse:
    res.headers["X-Test"] = "test"
    return createJsonResponse(res)


client: TestClient = TestClient(app)


def test_index():
    res: HttpxResponse = client.get("/")

    assert res.status_code == 200

    json: JsonResponse[Any] = JsonResponse[Any].model_validate(res.json())

    assert json.success == True


def test_fail():
    res: HttpxResponse = client.get("/fail")

    assert res.status_code == 400

    json: JsonResponse[Any] = JsonResponse[Any].model_validate(res.json())

    print(json)

    assert json.success == False

    assert json.errors is not None

    assert json.errors[0].code == "parse"
    assert json.errors[0].path == ["response"]
    assert json.errors[0].message == "response error"


def test_server_error():
    res: HttpxResponse = client.get("/server")

    assert res.status_code == 500

    json: JsonResponse[Any] = JsonResponse[Any].model_validate(res.json())

    assert json.success == False

    assert json.errors is not None

    assert json.errors[0].code == "server"
    assert json.errors[0].path == ["server"]
    assert json.errors[0].message == "server"


def test_header():
    res: HttpxResponse = client.get("/header")

    assert res.status_code == 200

    assert res.headers["X-Test"] == "test"
