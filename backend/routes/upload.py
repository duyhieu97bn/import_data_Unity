import os
import tempfile
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import Response
from services.excel_service import parse_records_from_file
from services.records_service import upsert_records
import config

router = APIRouter(prefix="/api", tags=["upload"])


@router.get("/template/download")
def download_template():
    path = os.path.abspath(config.TEMPLATE_FILE)
    if not os.path.exists(path):
        raise HTTPException(404, "File template không tồn tại")
    with open(path, "rb") as f:
        content = f.read()
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=template.xlsx",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
        }
    )


@router.post("/upload/preview")
async def preview_upload(file: UploadFile = File(...)):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(400, "Chỉ chấp nhận file Excel (.xlsx, .xls)")
    content = await file.read()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    tmp.write(content)
    tmp.close()
    try:
        records = parse_records_from_file(tmp.name)
    except Exception as e:
        os.unlink(tmp.name)
        raise HTTPException(400, f"Lỗi đọc file: {e}")
    os.unlink(tmp.name)
    return {"total": len(records), "records": records}


@router.post("/upload/confirm")
def confirm_upload(data: dict):
    records = data.get("records", [])
    if not records:
        raise HTTPException(400, "Không có dữ liệu để thêm")
    count = upsert_records(records)
    return {"status": "ok", "added": count}
