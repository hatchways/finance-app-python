import os
from functools import lru_cache

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from api.core.config import Settings
from api.routers import accounts, auth, transactions, users

load_dotenv()

app = FastAPI(
    title="Finance App Work Simulation - Python (FastAPI)",
    description="Finance App Work Simulation",
    version="0.0.1",
)


@lru_cache()
def get_settings():
    return Settings()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(transactions.router)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(_, exc):
    return JSONResponse({"error": exc.detail}, status_code=exc.status_code)


def main():
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=int(os.environ.get("PORT", "8080")),
    )


if __name__ == "__main__":
    main()
