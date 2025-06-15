---
title: FastAPI
description: FastAPI learning notes.
---

## Installation
```bash
# FastAPI depends on Pydantic and Starlette
pip install "fastapi[standard]"

# reads main.py file, detects the FastAPI app in it, and starts a server using Uvicorn
fastapi dev main.py
```

```python
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

## Interactive API docs
`/docs` shows the automatic interactive API documentation (provided by Swagger UI)

## Alternative API docs
`/redoc` shows the alternative automatic documentation (provided by ReDoc)

## Features
- Based on open standards
  - OpenAPI
  - Automatic data model documentation with JSON Schema
- Automatic docs
  - Swagger UI / ReDoc
-  based on standard Python type declarations (thanks to Pydantic)
-  Validation for most (or all?) Python data types and for more exotic types. All the validation is handled by Pydantic.
-  Security and authentication integrated. All the security schemes defined in OpenAPI
   -  HTTP Basic
   -  OAuth2 (also with JWT tokens) https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
   -  API keys in Headers, Query parameters and Cookies, etc
   -  Plus all the security features from Starlette (including session cookies)
-  Dependency Injection
-  Unlimited "plug-ins"
-  Starlette features
   -  FastAPI is actually a sub-class of Starlette
   -  WebSocket support
   -  In-process background tasks
   -  Startup and shutdown events
   -  Test client built on HTTPX
   -  CORS, GZip, Static Files, Streaming responses
   -  Session and Cookie support
   -  100% test coverage
   -  100% type annotated codebase
-  Pydantic features
   -  FastAPI is fully compatible with (and based on) Pydantic
   -  in many cases you can pass the same object you get from a request directly to the database, as everything is validated automatically
   -  in many cases you can just pass the object you get from the database directly to the client.

## Python Types
https://fastapi.tiangolo.com/python-types/

## Concurrency and async / await

 You can mix def and async def in your path operation functions as much as you need and define each one using the best option for you. FastAPI will do the right thing with them.