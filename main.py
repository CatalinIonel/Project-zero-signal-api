from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json

app = FastAPI()

@app.post("/signal")
async def receive_signal(request: Request):
    try:
        signal = await request.json()
        with open("latest_signal.json", "w") as f:
            json.dump(signal, f)
        return {"status": "received", "signal": signal}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/signal")
def get_signal():
    try:
        with open("latest_signal.json", "r") as f:
            signal = json.load(f)
        return signal
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"error": "No signal available"})
