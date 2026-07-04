#Pega os logs
from scr.LOGS import global_logs
import logging

logger = logging.getLogger(__name__)

#Define quais passos o pipeline vai seguir 
from scr.SCHEMA.transform import  Transform
from typing import Literal
import polars as pl

class Pipeline:
    def __init__(self, data:pl.LazyFrame, query:dict = None, status:str = None)->None:
        
        self.df = data
        self.query = query
        
    #Faz a limpeza de dados para a camada cleaned
    def cleaned(self) -> pl.LazyFrame:
        logger.info("Running the cleaned-layer transformation pipeline...")
        df = (Transform(data=self.df, schema=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base_volume",
            "taker_buy_quote_volume",
            "ignore",
        ]).
            Date(column_name="open_time").
            typing(column="open", type="float").
            typing(column="high", type="float").
            typing("low", type="float").
            typing("taker_buy_base_volume", type="float").
            typing("close", type="float").
            Drop(columns="open_time").
            Drop(columns="ignore").
              Order(column="Date", Descending=False).
              Shift(column="close", name="before_close").
              Percent(column="close", column_calculate="before_close", name="percent").
              build())
        logger.info("Cleaned-layer transformation completed.")
        return df
    
    #Faz as operações para a camada processed
    def processed(self) ->pl.LazyFrame:
        if self.query is not None:
             logger.info("Running the processed-layer query transformation...")
             df = Transform(data=self.df).Filter(Date=self.query["filter"], column="Date", field=self.query["field"]).Order(column="percent", Descending=False).build()
             logger.info("Processed-layer query transformation completed.")
             return df
         
        return Transform(data=self.df).Order(column="percent", Descending=False).build()
    
    
             
                 
             
            
            
        
        
        
        
    
        
