from fastapi import APIRouter
import db

router = APIRouter(prefix="/api", tags=["dashboard"])


@router.get("/dashboard/stats")
def dashboard_stats():
    conn = db.get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM records")
    total_contracts = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT hoTenKH) FROM records")
    total_customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM goi")
    total_packages = cur.fetchone()[0]

    cur.execute("SELECT COALESCE(SUM(tongTien), 0) FROM records")
    total_revenue = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM records WHERE tinhTrang LIKE 'Còn%'")
    active_contracts = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM records WHERE tinhTrang LIKE 'Hết hạn%' OR tinhTrang LIKE 'Da het%'")
    expired_contracts = cur.fetchone()[0]

    conn.close()
    return {
        "totalContracts": total_contracts,
        "totalCustomers": total_customers,
        "totalPackages": total_packages,
        "totalRevenue": total_revenue,
        "activeContracts": active_contracts,
        "expiredContracts": expired_contracts,
    }


@router.get("/dashboard/revenue-by-month")
def revenue_by_month():
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("SELECT nam, thang, COALESCE(SUM(tongTien), 0) AS total FROM records GROUP BY nam, thang ORDER BY nam, thang")
    rows = cur.fetchall()
    conn.close()
    labels = []
    values = []
    for r in rows:
        labels.append(f"T{r['thang']}/{r['nam']}")
        values.append(r['total'])
    return {"labels": labels, "values": values}


@router.get("/dashboard/top-sales")
def top_sales():
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("SELECT sale, COALESCE(SUM(tongTien), 0) AS total FROM records WHERE sale NOT IN ('','x','-') GROUP BY sale ORDER BY total DESC LIMIT 10")
    rows = cur.fetchall()
    conn.close()
    return {"labels": [r["sale"] for r in rows], "values": [r["total"] for r in rows]}


@router.get("/dashboard/package-distribution")
def package_distribution():
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("SELECT maGoi, COUNT(*) AS cnt FROM records GROUP BY maGoi ORDER BY cnt DESC LIMIT 10")
    rows = cur.fetchall()
    conn.close()
    return {"labels": [r["maGoi"] for r in rows], "values": [r["cnt"] for r in rows]}


@router.get("/dashboard/contract-status")
def contract_status():
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM records WHERE tinhTrang LIKE 'Còn%'")
    active = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM records WHERE tinhTrang LIKE '%hết hạn%' OR tinhTrang LIKE 'Da het%'")
    expired = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM records WHERE tinhTrang = '' OR tinhTrang IS NULL")
    unknown = cur.fetchone()[0]
    conn.close()
    return {"labels": ["Còn hạn", "Hết hạn", "Khác"], "values": [active, expired, unknown]}


@router.get("/dashboard/revenue-by-clb")
def revenue_by_clb():
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("SELECT clb, COALESCE(SUM(tongTien), 0) AS total FROM records WHERE clb NOT IN ('','x','-') GROUP BY clb ORDER BY total DESC")
    rows = cur.fetchall()
    conn.close()
    return {"labels": [r["clb"] for r in rows], "values": [r["total"] for r in rows]}


@router.get("/dashboard/new-contracts-by-month")
def new_contracts_by_month():
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("SELECT nam, thang, COUNT(*) AS cnt FROM records GROUP BY nam, thang ORDER BY nam, thang")
    rows = cur.fetchall()
    conn.close()
    labels = []
    values = []
    for r in rows:
        labels.append(f"T{r['thang']}/{r['nam']}")
        values.append(r['cnt'])
    return {"labels": labels, "values": values}


@router.get("/dashboard/customer-source")
def customer_source():
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(NULLIF(nguon,''), 'Không rõ') AS nguon, COUNT(*) AS cnt FROM records GROUP BY nguon ORDER BY cnt DESC")
    rows = cur.fetchall()
    conn.close()
    return {"labels": [r["nguon"] for r in rows], "values": [r["cnt"] for r in rows]}
