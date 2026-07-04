from typing import Optional
from fastapi import APIRouter
from scr.CONTROLLER.handle import Handle
Router = APIRouter(
    prefix="/bitcoin",
    tags=["bitcoin"]
)

@Router.get("/")
def Query(filter: Optional[str] = None, field: Optional[str] = None):
    return Handle().HandleQuery(
        field=field,
        filter=filter
    )

@Router.get("/status")
def Status(id:str):
    return Handle().HandleStatusSave(
        id=id
    )
    
    

