#Cria o variavel pra chamar os logs
from scr.LOGS import global_logs
import logging

logger = logging.getLogger(__name__)

#Manipula os dataframes
import polars as pl
from typing import Literal

class Transform:
    def __init__(self, data: dict|pl.LazyFrame, schema:list = None) ->None:
        self.data = data
        self.schema = schema
        self.df = self.to_lf()
        
    #Transforma em Lazyframe caso os dados sejam um dicionario
    def to_lf(self) -> pl.LazyFrame|pl.LazyFrame:
        if isinstance(self.data, dict) | isinstance(self.data, list):
            logger.info("Converting input data to a LazyFrame...")
            df= pl.LazyFrame(self.data, schema=self.schema, orient="row")
            logger.info("Input data converted to a LazyFrame.")
            return df
        
        
        return self.data
    
    #Converte uma coluna pra data
    def Date(self, column_name:str) -> Transform|pl.LazyFrame:
        
        #Confere se a coluna existe
        logger.info(f"Checking whether column '{column_name}' exists...")
        
        if column_name in self.df.collect_schema().names():
            
            logger.info(f"Column '{column_name}' found.")
            
        else:
            
            logger.error(f"Column '{column_name}' was not found.")
            raise KeyError("Column does not exist")
        
        self.df = self.df.with_columns(
            pl.from_epoch(column_name, time_unit="ms").dt.date().alias("Date")
            
        )
       
        
        
        return self
    
    #Filtra os dados
    def Filter(self, column:str, field:str|int|float, Date:Literal["year", "month", "day"] = None) ->Transform|pl.LazyFrame:
        logger.info(f"Filtering data by column '{column}'...")
        
        if Date is not None:
            if Date == "year":
                df = self.df.filter(
            pl.col(column).dt.year() == field
        ) 
            elif Date == "month":
                df = self.df.filter(
            pl.col(column).dt.month() == field
            
        ) 
            else:
                df = self.df.filter(
            pl.col(column).dt.day() == field
        ) 
        
        else:
            
            df = self.df.filter(
                pl.col(column) == field
            ) 
            
        logger.info("Data filtering completed.")
        
        self.df = df
        return self
    
    
    #Faz os calculos de agrupamento
    def group_operation(self,column:str, mean:str, max:str, min:str, count:str) ->Transform|pl.LazyFrame:
        logger.info("Running aggregation operations...")
        df = self.df.group_by(column).agg(
            pl.col(mean).mean().alias(f"mean_{mean}"),
            pl.col(max).max().alias(f"max_{max}"),
            pl.col(min).min().alias(f"min_{min}"),
            pl.col(count).count().alias(f"count_{count}")
        )
        logger.info("Aggregation operations completed.")
        self.df = df
        return self
    
    #deleta as colunas
    def Drop(self, columns:list|str) -> Transform|pl.LazyFrame:
        logger.info(f"Dropping column(s): {columns}...")
        df = self.df.drop(columns)
        logger.info("Column removal completed.")
        self.df = df
        return self
    
    def typing(self, column:str, type:Literal[
        "str",
        "int",
        "float",
        "bool",
        "bytes",
        "list",
        "dict",
        "object",
        "None",
    ]) -> Transform|pl.LazyFrame:
      

        TYPE_MAPPING = {
            "str": pl.String,
            "int": pl.Int64,
            "float": pl.Float64,
            "bool": pl.Boolean,
            "bytes": pl.Binary,
            "list": pl.List,
            "dict": pl.Struct,
            "object": pl.Object,
            "None": pl.Null,
        }  
        logger.info(f"Casting column '{column}' to {type}...")
        df = self.df.with_columns(
            pl.col(column).cast(TYPE_MAPPING[type])
        )
        logger.info(f"Column '{column}' cast completed.")
        self.df = df
        return self
    
    #diminui as casas decimais das colunas que são float
    def round(self) -> Transform|pl.LazyFrame:
        logger.info("Rounding floating-point columns...")
        schema = self.df.collect_schema()
        columns = [c for c in schema.names() if schema[c] == pl.Float64]
        for c in columns:
            df = self.df.with_columns(
                pl.col(c).round(2)
            )
            
        logger.info("Floating-point column rounding completed.")
       
        return self
    
    
    #Muda o nome das colunas do dicionario
    def rename(self, names:dict) ->Transform|pl.LazyFrame:
        logger.info(f"Renaming columns: {'.'.join(list(names.keys()))}...")
        self.df = self.df.rename(
            names
        )
        logger.info("Column renaming completed.")
        return self
    
    def build(self) -> pl.LazyFrame:
        return self.df
    
    #Empurra uma coluna pra baixo
    def Shift(self, column:str, name:str) ->Transform|pl.LazyFrame:
        from datetime import date
        logger.info(f"Creating column '{name}'...")
        if self.df.collect_schema()[column] == pl.Date:
            self.df = self.df.with_columns(
                pl.col(column).shift(1).fill_null(date(1,1,1)).alias(name)
            )
        else:
            self.df = self.df.with_columns(
                pl.col(column).shift(1).fill_null(0).alias(name)
            )
        logger.info(f"Column '{name}' created.")
        
        return self
    
    #Orderna do maior pro menor
    def Order(self, column:str, Descending:bool)  ->Transform|pl.LazyFrame:
        logger.info(f"Sorting data by column '{column}'...")
        self.df = self.df.sort(column, descending=Descending)
        logger.info("Data sorting completed.")
        return self
    
    
    #Calcula o percental de crescimento
    def Percent(self, column: str, column_calculate: str, name: str):
        self.df = self.df.with_columns(
            pl.when(pl.col(column) == 0)
            .then(None)
            .otherwise(
                ((pl.col(column_calculate) - pl.col(column)) / pl.col(column)) * 100
            )
            .round(2)
            .alias(name)
        )

        return self
    
    
    
    
        
    
    
    
    
    
        
    
        
        
        
        
        
        
    
        
        
        

        
