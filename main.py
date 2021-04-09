from fastapi import FastAPI
from typing import Optional
from packages import web_activity
from packages import worker_activity
from packages import machines

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Welcome to the SDH Activity API"}



@app.get("/machines/{machine_id}")
def get_item(machine_id: int):
    if machine_id:
        return machines.Machine(machine_id=machine_id)
    return machine_id

@app.post("/web_activity")
async def web_event(event: web_activity.WebActivity):
    insert = event.insert_record()
    result = {"status": insert, "payload": event.dict()}
    return result


@app.post("/worker_activity")
async def worker_event(event: worker_activity.WorkerActivity):
    insert = event.insert_record()
    payload = event.dict()
    result = {"status": insert, "payload":payload}
    return result