import os
import sys
import uvicorn

client_path = os.path.join(os.path.dirname(__file__), 'client')
sys.path.insert(0, client_path)

if __name__ == "__main__":
    print("Starting FastAPI Server...")
    print("Server will be available at: http://127.0.0.1:8000")
    print("Press Ctrl+C to stop")
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[client_path]
    ) 