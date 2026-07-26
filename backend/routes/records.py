from fastapi import APIRouter, HTTPException
from schemas import RecordData
from services.records_service import get_all_records, add_record, update_record, delete_record

router = APIRouter(prefix="/api", tags=["records"])


@router.get("/records")
def list_records():
    return get_all_records()


@router.post("/records")
def create_record(record: RecordData):
    return add_record(record.model_dump())


@router.put("/records/{stt}")
def edit_record(stt: int, record: RecordData):
    ok = update_record(stt, record.model_dump())
    if not ok:
        raise HTTPException(404, "Không tìm thấy bản ghi")
    return {"status": "updated", "stt": stt}


@router.delete("/records/{stt}")
def remove_record(stt: int):
    ok = delete_record(stt)
    if not ok:
        raise HTTPException(404, "Không tìm thấy bản ghi")
    return {"status": "deleted", "stt": stt}
