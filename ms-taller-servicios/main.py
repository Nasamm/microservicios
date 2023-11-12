from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import servicios

app = FastAPI(title="ms-taller-servicios")


origins =  [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(servicios.router)

init_db()