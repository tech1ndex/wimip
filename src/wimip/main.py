from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def read_root(request: Request):
    client_host = request.client.host
    return {f"Your IP: {client_host}"}