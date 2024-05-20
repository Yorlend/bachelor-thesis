from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.APRouter import APRouter
from api.routers.FpRouter import FpRouter
from api.routers.LocalizationRouter import LocalizationRouter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(FpRouter)
app.include_router(LocalizationRouter)
app.include_router(APRouter)
