from fastapi import FastAPI

from api.routers.APRouter import APRouter
from api.routers.FpRouter import FpRouter
from api.routers.LocalizationRouter import LocalizationRouter

app = FastAPI()
app.include_router(FpRouter)
app.include_router(LocalizationRouter)
app.include_router(APRouter)
