[< Back](./../README.md)

# JDER FastAPI

A response builder for FastAPI.

## Installation

Install this package as a dependency in the project:

> This package requires `fastapi` to be installed.

```sh
# pip
pip install jder-fastapi

# uv
uv add jder-fastapi

# Pixi
pixi add --pypi jder-fastapi
```

## Create a Success JSON Response

To create a JSON response without data, just use `createJsonResponse` function:

```python
from fastapi import FastAPI
from fastapi.responses import Response
from jder_fastapi.responses.json import createJsonResponse

app: FastAPI = FastAPI()


@app.get("/")
async def route() -> Response:
    return createJsonResponse()
```

And the response will be shown as below:

```json
{
    "success": true
}
```

## Create a Success JSON Response with Data

The `createJsonResponse` function can also be used to insert data to the response:

```python
from fastapi import FastAPI
from fastapi.responses import Response
from jder_fastapi.responses.json import (
    createJsonResponse,
    createJsonSuccessResponseOptions,
)

app: FastAPI = FastAPI()


@app.get("/")
async def route() -> Response:
    return createJsonResponse(
        options=createJsonSuccessResponseOptions(
            data="Hello, World!",
        ),
    )
```

And the response will be shown as below:

```json
{
    "success": true,
    "data": "Hello, World!"
}
```

## Create a Failure JSON response

To create a failure JSON response, add `error` field to the options:

```python
from fastapi import FastAPI
from fastapi.responses import Response
from jder_fastapi.responses.json import (
    createJsonResponse,
    createJsonFailureResponseOptions,
    JsonResponseError,
)

app: FastAPI = FastAPI()


@app.get("/")
async def route() -> Response:
    return createJsonResponse(
        options=createJsonFailureResponseOptions(
            status=500,
            errors=[
                JsonResponseError(
                    code="server",
                ),
            ],
        ),
    )
```

And the response will be shown as below:

```json
{
    "success": false,
    "errors": [
        {
            "code": "server"
        }
    ]
}
```

## Combine additional headers from the response

To combine additional headers from the response, add `response` to the function:

```python
from fastapi import FastAPI
from fastapi.responses import Response
from jder_fastapi.responses.json import (
    createJsonResponse,
    createJsonSuccessResponseOptions,
)

app: FastAPI = FastAPI()


@app.get("/")
async def route(res: Response) -> Response:
    
    res.headers["X-Test"] = "Hello, World!"

    return createJsonResponse(
        res,
        createJsonSuccessResponseOptions(
            data="Hello, World!",
        ),
    )
```

## Create a Non-JSON response

To create a non-JSON response, use `createResponse` function:

```python
from fastapi import FastAPI
from fastapi.responses import Response
from jder_fastapi.responses import (
    createResponse,
    createResponseOptions,
)

app: FastAPI = FastAPI()


@app.get("/")
async def route() -> Response:
    return createResponse(
        options=createResponseOptions(
            status=404,
            headers={
                "Content-Type": "text/plain",
            },
            body="Not Found",
        ),
    )
```

## Request Validation Exception Handler

Enforce a validation exception handler to return a JSON response:

```python
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.exceptions import RequestValidationError
from jder_fastapi.handlers import request_validation_exception_handler

app: FastAPI = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    req: Request,
    exc: RequestValidationError
) -> Response:
    return request_validation_exception_handler(req, exc)
```
