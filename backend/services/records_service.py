import db
from .excel_service import RECORD_COLS


def get_all_records():
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT {','.join(RECORD_COLS)} FROM records ORDER BY stt")
    rows = cur.fetchall()
    conn.close()
    return [dict(zip(RECORD_COLS, r)) for r in rows]


def add_record(record: dict):
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(MAX(stt), 0) + 1 FROM records")
    next_stt = cur.fetchone()[0]
    record["stt"] = next_stt
    cols = RECORD_COLS
    placeholders = ",".join("?" for _ in cols)
    vals = [record.get(c, "") for c in cols]
    cur.execute(f"INSERT INTO records ({','.join(cols)}) VALUES ({placeholders})", vals)
    conn.commit()
    conn.close()
    return record


def update_record(stt: int, record: dict):
    conn = db.get_conn()
    cur = conn.cursor()
    sets = ",".join(f"{c}=?" for c in RECORD_COLS)
    vals = [record.get(c, "") for c in RECORD_COLS]
    cur.execute(f"UPDATE records SET {sets} WHERE stt=?", vals + [stt])
    conn.commit()
    conn.close()
    return cur.rowcount > 0


def delete_record(stt: int):
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM records WHERE stt=?", (stt,))
    ok = cur.rowcount > 0
    conn.commit()
    conn.close()
    return ok


def upsert_records(new_records: list):
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(MAX(stt), 0) + 1 FROM records")
    next_stt = cur.fetchone()[0]
    cols = RECORD_COLS
    placeholders = ",".join("?" for _ in cols)
    sql = f"INSERT INTO records ({','.join(cols)}) VALUES ({placeholders})"
    count = 0
    for i, rec in enumerate(new_records):
        rec["stt"] = next_stt + i
        vals = [rec.get(c, "") for c in cols]
        cur.execute(sql, vals)
        count += 1
    conn.commit()
    conn.close()
    return count
