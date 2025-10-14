from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import students

app = FastAPI(title="Student Management API")

# CORS không bắt buộc với Desktop App, nhưng để mở cho tiện khi test
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(students.router)