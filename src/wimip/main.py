from fastapi import FastAPI, Depends, Header

app = FastAPI()

@app.get("/")
def xff_ip(real_ip: str = Header(None, alias='x-forwarded-for')):
    return real_ip