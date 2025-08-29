from fastapi import FastAPI
from fastapi.responses import Response as FastApiResponse
from fastapi.testclient import TestClient
from httpx import Response as HttpxResponse
from jder_fastapi.responses import CreateResponseOptions, createResponse

app: FastAPI = FastAPI()


@app.get("/")
async def index(res: FastApiResponse) -> FastApiResponse:
    return createResponse(
        res,
        CreateResponseOptions(
            status=201,
            headers={"Content-Type": "text/plain"},
            body="Hello, World!",
        ),
    )


@app.get("/header")
async def header(res: FastApiResponse) -> FastApiResponse:
    res.headers["X-Test"] = "test"
    return createResponse(res)


client: TestClient = TestClient(app)


def test_index():
    res: HttpxResponse = client.get("/")
    assert res.status_code == 201
    assert res.headers["Content-Type"] == "text/plain"
    assert res.text == "Hello, World!"


def test_header():
    res: HttpxResponse = client.get("/header")
    assert res.status_code == 200
    assert res.headers["X-Test"] == "test"
