#Pega os logs
from scr.LOGS import global_logs
import logging

logger = logging.getLogger(__name__)

#Serve pra orquestrar todo o pipeline e chamar as camadas anteriores
from scr.INFRA.manager import RequestData, app
from scr.ADAPTER.DATABASE.manager import Layer
from scr.SCHEMA.transform import Transform
from typing import Literal
from celery.result import AsyncResult
import polars as pl
from scr.SERVICE.pipeline import Pipeline
from typing import Literal
from scr.SERVICE.task import Save
class Query:
    def __init__(self,  filter:Literal["year", "month", "day"]= None, field:str = None)->None:
        
        self.filter = filter
        self.filed = field
        
     #Chama a task para salvar   
    def save(self, status:Literal["raw", "cleaned", "processed", "request"]):
        data = {
            "raw": ["cleaned", "processed"],
            "cleaned": ["processed"],
            "processed": None,
            "request": ["raw", "cleaned", "processed"]
        }
        if data[status] is not None:
            logger.info(f"Starting task to save the following layer(s): {','.join(data[status])}...")
            task = Save.delay(status)
            return task.id
        
        logger.info("All layers already contain data; no save task was started.")
        return None
        
    #le os dados e retorna o lazyframe e a camada que esta  
    def read(self) -> dict:
        data = {
            "processed": Layer(layer="processed").read_partition,
            "cleaned": Layer("cleaned").read,
            "raw": Layer("raw").read,
            "request": RequestData().Get
        }
        
        for c, v in data.items():
            if c == "processed":
                get = v(partition="Date")
                
            else:
                get = v()
                
            if get is not None:
                status = c
                break
        return {"status": status, "data":get}
    
    
        
       
    #Orquestra tudo
    def execute(self) -> pl.LazyFrame|dict:
        
        data = self.read()
        df = data["data"]
        status = data["status"]
        task_save = self.save(status=status)
        
        if status == "processed" or status == "cleaned":
            df = Pipeline(data=df, query={"filter":self.filter, "field":self.filed}).processed() if self.filter is not None else Pipeline(data=df).processed()
            return df.collect().to_dicts() if status == "processed" else {
                "task_id": task_save,
                "data": df.collect().to_dicts()
            }
        
        df = Pipeline(data=df).cleaned()
        df = Pipeline(data=df, query={"filter":self.filter, "field":self.filed}).processed() if self.filter is not None else Pipeline(data=df).processed()
        return  {
                "task_id": task_save,
                "data": df.collect().to_dicts()
            }
        
    def status_task(self, id:str) -> str:
        return AsyncResult(
            id=id,
            app=app
        )
        
    
        
        
        
            
            
        
        
        
        
       
        
        
        
        
        
        
        
        
        
            
    
            
            
            
            
            
            
            
            
                
                
                
            
            
            
            
        
            
        
            
    
    
                
                
            
        
        

        
        
    
