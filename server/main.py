from fastapi import FastAPI

from core.config import settings
import uvicorn

from routers import role

app = FastAPI(title="PZ-2 HeadHunter API", debug=settings.debug)

app.include_router(role.router)

@app.get("/")
async def root():
    return {
        "message": "PZ-2 FastAPI server started",
        "config": {
            "port": settings.port,
            "db_host": settings.db_host
        }
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=settings.debug)