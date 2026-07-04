from scr.CONTROLLER.router import Router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router=Router)