import os
import tempfile
from fastapi import APIRouter, HTTPException, UploadFile, File
from schemas import GoiData
from services.goi_service import get_goi_list, get_goi_detail, create_goi, update_goi, delete_goi, import_goi_from_file, get_sale_list, get_pt_cham_soc_list, get_cs_nhap_list

router = APIRouter(prefix="/api", tags=["goi"])


@router.get("/goi")
def list_goi():
    return get_goi_list()


@router.get("/goi/{ma_goi}")
def detail_goi(ma_goi: str):
    detail = get_goi_detail(ma_goi)
    if not detail:
        raise HTTPException(404, "Mã gói không tồn tại")
    return detail


@router.post("/goi")
def add_goi(data: GoiData):
    return create_goi(data.model_dump())


@router.put("/goi/{goi_id}")
def edit_goi(goi_id: int, data: GoiData):
    ok = update_goi(goi_id, data.model_dump())
    if not ok:
        raise HTTPException(404, "Không tìm thấy gói")
    return {"status": "updated", "id": goi_id}


@router.delete("/goi/{goi_id}")
def remove_goi(goi_id: int):
    ok = delete_goi(goi_id)
    if not ok:
        raise HTTPException(404, "Không tìm thấy gói")
    return {"status": "deleted", "id": goi_id}


@router.get("/sale")
def sale_list():
    return get_sale_list()


@router.get("/pt-cham-soc")
def pt_cham_soc_list():
    return get_pt_cham_soc_list()


@router.get("/cs-nhap")
def cs_nhap_list():
    return get_cs_nhap_list()


@router.post("/goi/import")
async def import_goi(file: UploadFile = File(...)):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(400, "Chỉ chấp nhận file Excel (.xlsx, .xls)")
    content = await file.read()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    tmp.write(content)
    tmp.close()
    try:
        imported, total = import_goi_from_file(tmp.name)
    except Exception as e:
        os.unlink(tmp.name)
        raise HTTPException(400, f"Lỗi đọc file: {e}")
    os.unlink(tmp.name)
    return {"status": "ok", "imported": imported, "total": total}
