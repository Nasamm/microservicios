from fastapi import FastAPI
from routers import clientes
from fastapi.middleware.cors import CORSMiddleware
from database import init_db

app = FastAPI(title="ms-taller-clientes")

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

app.include_router(clientes.router)

init_db()