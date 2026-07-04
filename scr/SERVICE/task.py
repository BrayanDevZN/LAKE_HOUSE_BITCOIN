from scr.INFRA.manager import app, RequestData
import polars as pl

from typing import Literal
from scr.SERVICE.pipeline import Pipeline
from scr.ADAPTER.DATABASE.manager import Layer

#Essa task serve pra salvar os dados, ela le os dados apartir da camada que ele esta, e vai salvando nas camadas posteriores
@app.task(bind=True, max_retries=3)
def Save(task, layer:Literal["request", "raw", "cleaned", "processed"]):
    data = {
            
            "cleaned": Layer(layer="cleaned").read,
            "raw": Layer("raw").read,
            "request": RequestData().Get
        }
    
    if layer == "processed":
        return 
    
    df = data[layer]()
    
    if layer == "request":
        Layer(layer="raw").save(df)
        df = Pipeline(data=df).cleaned()
        Layer(layer="cleaned").save(data=df)
        Layer(layer="processed").partition(data=df, column="Date")
        
    if layer == "raw":
        df = Pipeline(data=df).cleaned()
        Layer(layer="cleaned").save(data=df)
        Layer(layer="processed").partition(data=df, column="Date")
        
    if layer == "cleaned":
        Layer(layer="processed").partition(data=df, column="Date")
        
    return True
        
        
        
        
    
        
    
        
    
        
    
    
    
        
        
        
        
    
    

