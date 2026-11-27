from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Stick Battle API")

# Địa chỉ frontend (Live Server) được phép gọi API
FRONTEND_ORIGINS = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

# Các phương thức HTTP mà API sử dụng
ALLOWED_METHODS = ["GET", "POST"]

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOWED_METHODS,
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Stick Battle API is running"}


@app.get("/api/health", tags=["System"])
def health_check():
    return {"status": "ok", "service": "Stick Battle API"}