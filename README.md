# build và chạy toàn bộ hệ thống

```
docker-compose up --build
```

FastAPI chạy tại: http://localhost:8000

Swagger docs: http://localhost:8000/docs

```
fastapi_backend/
├── app/
│   ├── api/               # Router endpoints (auth, user, etc.)
│   ├── core/              # Cấu hình chung, JWT helper
│   ├── db/                # Kết nối & init database
│   ├── models/            # ORM models (SQLAlchemy)
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic (Register/Login)
├── main.py                # Điểm khởi đầu
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md              # (chính là bạn đang đọc)

```
