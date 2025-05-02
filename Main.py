from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

app = FastAPI()
latest_signal = {}

class Signal(BaseModel):
    symbol: str
    action: str
    lot_size: float
    sl: float
    tp: float

@app.post("/signal")
async def receive_signal(signal: Signal):
    global latest_signal
    latest_signal = signal.dict()
    return {"status": "received", "signal": latest_signal}

@app.get("/latest")
async def get_latest_signal():
    if not latest_signal:
        raise HTTPException(status_code=404, detail="No signal available")
    return latest_signal
