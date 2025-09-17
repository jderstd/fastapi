# JDER FastAPI

A response builder for FastAPI.

This package includes different response builders based on the JSON response structure specified in [JSON Data Errors Response (JDER)](https://github.com/jderstd/spec). With the builders, various kinds of responses can be created easily instead of sending plain text responses.

## Quick Start

To create a JSON response, use the following code:

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

## License

This project is licensed under the terms of the MIT license.
