from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.records import router as records_router
from routes.goi import router as goi_router
from routes.upload import router as upload_router
import config
import db

app = FastAPI(title="Excel Data Entry API")


@app.on_event("startup")
def startup():
    db.init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(records_router)
app.include_router(goi_router)
app.include_router(upload_router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
