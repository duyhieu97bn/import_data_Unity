import db
from .excel_service import GOI_COLS, parse_goi_from_file


def get_goi_list():
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT id,{','.join(GOI_COLS)} FROM goi ORDER BY maGoi")
    rows = cur.fetchall()
    conn.close()
    result = []
    for r in rows:
        item = dict(zip(["id"] + GOI_COLS, r))
        result.append(item)
    return result


def get_goi_detail(ma_goi: str):
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT id,{','.join(GOI_COLS)} FROM goi WHERE maGoi=?", (ma_goi,))
    r = cur.fetchone()
    conn.close()
    return dict(zip(["id"] + GOI_COLS, r)) if r else None


def create_goi(data: dict):
    conn = db.get_conn()
    cur = conn.cursor()
    cols = GOI_COLS
    placeholders = ",".join("?" for _ in cols)
    vals = [data.get(c, "") for c in cols]
    cur.execute(f"INSERT INTO goi ({','.join(cols)}) VALUES ({placeholders})", vals)
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return {**data, "id": last_id}


def update_goi(goi_id: int, data: dict):
    conn = db.get_conn()
    cur = conn.cursor()
    sets = ",".join(f"{c}=?" for c in GOI_COLS)
    vals = [data.get(c, "") for c in GOI_COLS]
    cur.execute(f"UPDATE goi SET {sets} WHERE id=?", vals + [goi_id])
    conn.commit()
    conn.close()
    return cur.rowcount > 0


def delete_goi(goi_id: int):
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM goi WHERE id=?", (goi_id,))
    ok = cur.rowcount > 0
    conn.commit()
    conn.close()
    return ok


def import_goi_from_file(filepath: str):
    items = parse_goi_from_file(filepath)
    conn = db.get_conn()
    cur = conn.cursor()
    count = 0
    for item in items:
        placeholders = ",".join("?" for _ in GOI_COLS)
        vals = [item.get(c, "") for c in GOI_COLS]
        try:
            cur.execute(f"INSERT OR IGNORE INTO goi ({','.join(GOI_COLS)}) VALUES ({placeholders})", vals)
            if cur.rowcount > 0:
                count += 1
        except Exception:
            pass
    conn.commit()
    conn.close()
    return count, len(items)


def get_unique_column_values(col):
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT DISTINCT {col} FROM records WHERE {col} NOT IN ('','x','X','None','-','xxx') AND {col} IS NOT NULL ORDER BY {col}")
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]


def get_sale_list():
    return get_unique_column_values("sale")


def get_pt_cham_soc_list():
    return get_unique_column_values("ptChamSoc")


def get_cs_nhap_list():
    return get_unique_column_values("csNhap")
