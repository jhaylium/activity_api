from fastapi import APIRouter
from app.models import machines

router = APIRouter()

@router.get("/machines/{machine_id}")
def get_item(machine_id: int):
    if machine_id:
        return machines.Machine(machine_id=machine_id)
    return machine_id