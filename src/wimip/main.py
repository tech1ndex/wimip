from fastapi import FastAPI, Depends, Header, Request
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()
routes_to_reroute = ["/"]

class Details(BaseModel):
    ip: int | None = None
    user_agent: str | None = None
    method: str | None = None
    referrer: str | None = None

@app.middleware("http")
async def redirect_middleware(request: Request, call_next):
    if request.url.path in routes_to_reroute:
        request.scope["path"] = "/ip"
        headers = dict(request.scope['headers'])
        headers[b'custom-header'] = b'my custom header'
        request.scope['headers'] = [(k, v) for k, v in headers.items()]

    return await call_next(request)


@app.get("/")
async def main():
    return {"message": "OK"}


@app.get("/ip")
def client_ip(xff_ip: int = Header(None, alias='x-forwarded-for')):
    return xff_ip

@app.get("/details", response_model=Details)
def client_details(xff_ip: int = Header(None, alias='x-forwarded-for'),
                   request_ref: str = Header(None, alias='referrer'),
                   user_agent: Annotated[str | None, Header()] = None):
    return Details(ip=xff_ip,
                   user_agent=user_agent,
                   method="GET",
                   referrer=request_ref)