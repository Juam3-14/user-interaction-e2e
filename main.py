from fastapi import FastAPI
from routers import routers_v1

app = FastAPI(
    title="user-interaction-e2e",
    version="v1"
)

app.include_router(routers_v1.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}