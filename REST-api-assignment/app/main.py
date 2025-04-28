from fastapi import FastAPI
import uvicorn
from app.routers.item_router import router as item_router

def create_app() -> FastAPI:
    app = FastAPI(title="Simple CRUD API")
    
    app.include_router(item_router)
    
    @app.get("/")
    def root():
        return {"status": "API is running"}
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)