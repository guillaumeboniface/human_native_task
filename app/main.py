from fastapi import FastAPI
from app.api import violation
from app.core.rate_limiter import rate_limit_middleware

app = FastAPI(title="Violation API")
app.middleware("http")(rate_limit_middleware)
app.include_router(violation.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)