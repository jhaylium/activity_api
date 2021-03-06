from fastapi import APIRouter
from app.models import web_activity, worker_activity, event

router = APIRouter()

@router.post("/web_activity")
async def web_event(event: web_activity.WebActivity):
    insert = event.insert_record()
    result = {"status": insert, "payload": event.dict()}
    return result


@router.post("/worker_activity")
async def worker_event(event: worker_activity.WorkerActivity):
    insert = event.insert_record()
    payload = event.dict()
    result = {"status": insert, "payload": payload}
    return result

@router.post("/event")
async def event_activity(event_x: event.EventActivity):
    insert = event_x.insert_record()
    payload = event_x.dict()
    result = {"status": insert, "payload": payload}
    return result