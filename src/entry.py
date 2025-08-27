import uvicorn
from app import App

if __name__ == "__main__":
    app = App()
    uvicorn.run(app.get_app(), host="0.0.0.0", port=8000, log_level="info")
