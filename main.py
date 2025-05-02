from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
import os

app = FastAPI()

SIGNAL_FILE = "latest_signal.json"

@app.post("/signal")
async def receive_signal(request: Request):
    try:
        signal = await request.json()
        with open(SIGNAL_FILE, "w") as f:
            json.dump(signal, f)
        return {"status": "received", "signal": signal}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/signal")
def get_signal():
    if os.path.exists(SIGNAL_FILE):
        try:
            with open(SIGNAL_FILE, "r") as f:
                signal = json.load(f)
            return {"status": "ok", "signal": signal}
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": f"Failed to read signal: {str(e)}"})
    else:
        return JSONResponse(status_code=404, content={"error": "No signal available"})
