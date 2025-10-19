from fastapi import FastAPI, status
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class HealthResponse(BaseModel):
    status: str
    service: str = "model-serving-server"
    version: str = "0.1.0"

@app.get("/healthz", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def healthz():
    return HealthResponse(status="healthy")

def main():
    """
    Main function to run the FastAPI server
    """
    print("Starting Model Serving Server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    main()
