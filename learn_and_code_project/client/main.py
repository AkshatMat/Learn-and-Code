import os
import uvicorn
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from client.server.fast_api.routers import admin_login
from client.server.fast_api.routers import user_login
from client.server.fast_api.routers import signup
from client.server.fast_api.routers import headlines
from client.server.fast_api.routers import saved_articles

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Server is running on http://127.0.0.1:{port}")
    yield

app = FastAPI(
    title="Taaza Khabar",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(signup.router, prefix="/signup_user", tags=["signup"])
app.include_router(admin_login.router, prefix="/login_admin", tags=["login"])
app.include_router(user_login.router, prefix="/login_user", tags=["login"])
app.include_router(headlines.router, prefix="/headlines", tags=["headlines"])
app.include_router(saved_articles.router, prefix="/articles", tags=["Saved Articles"])

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting server on http://127.0.0.1:{port}")
    uvicorn.run("client.main:app", host="127.0.0.1", port=port, reload=True)
