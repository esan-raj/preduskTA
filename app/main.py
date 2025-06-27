from fastapi import FastAPI
from .routes import router

app = FastAPI(title="preduskTA - Book Review Service")

app.include_router(router)