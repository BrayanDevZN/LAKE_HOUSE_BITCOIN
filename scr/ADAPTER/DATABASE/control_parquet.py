#Pega os logs
from scr.LOGS import global_logs
import logging

logger = logging.getLogger(__name__)

#Salva os arquivos em parquet em ADAPTER/STORAGE/CLEANED ou ADAPTER/STORAGE/PROCESSED ou le
import polars as pl
class ControlParquet:
    def __init__(self, layer:str)->None:
        self.layer = layer
        
    def save(self, data:dict|pl.LazyFrame) -> None | bool:
        try:
            
            
            if isinstance(data, dict):
                
                logger.info("Input data is a dictionary; converting it to a DataFrame...")
                df = pl.DataFrame(data)
                
                
            else:
                logger.info("Input data is a LazyFrame; converting it to a DataFrame...")
                df = data.collect()
                
            logger.info("Input data converted to a DataFrame.")
            
            logger.info(f"Saving Parquet file to layer '{self.layer}'...")
                 
            df.write_parquet(f"{self.layer}/data.parquet")
            
            return True
        
        except Exception as e:
            logger.error(f"Failed to save the Parquet file to layer '{self.layer}'.")
            raise ValueError(e)
        
        
    def read(self) -> pl.LazyFrame | None:
        try:
            import os
            logger.info(f"Reading Parquet file from layer '{self.layer}'...")
            
            #Confere se o arquivo existe
            if not os.path.exists(f"{self.layer}/data.parquet"):
                logger.info(f"No Parquet file was found in layer '{self.layer}'.")
                return None
            
            return pl.scan_parquet(f"{self.layer}/data.parquet")
        
        except Exception as e:
            logger.error(f"Failed to read the Parquet file from layer '{self.layer}'.")
            raise ValueError(e)
    
    #Partiona os dados
    def partition(self, column:str|list, data:dict|pl.LazyFrame) -> None :
        try:
            #Confere se a coluna existe
            logger.info(f"Checking whether partition column '{column}' exists...")
            
            schema = data.collect_schema()
            if column in schema.names():
                
                logger.info(f"Partition column '{column}' found.")
                
                #Deleta o caminho caso não exista
                import os
                import shutil

                logger.info(f"Checking for an existing partition in layer '{self.layer}'...")
                if os.path.exists(f"{self.layer}/{column}"):
                    shutil.rmtree(f"{self.layer}/{column}")
                    logger.info("Existing partition directory removed before rewrite.")
                
                
                
            else:
                
                logger.error(f"Partition column '{column}' was not found.")
                raise KeyError("Column does not exist")
            
            if isinstance(data, dict):
                
                logger.info("Input data is a dictionary; converting it to a DataFrame...")
                df = pl.DataFrame(data)
                
                
            else:
                logger.info("Input data is a LazyFrame; converting it to a DataFrame...")
                df = data.collect()
                
            logger.info("Input data converted to a DataFrame.")
            
            
           
            df.write_parquet(
                f"{self.layer}/{column}",
                partition_by=[column] if isinstance(column, str) else column
            )
        except Exception as e:
            logger.error(f"Failed to write partitioned data to layer '{self.layer}'.")
            raise ValueError(e)
        
    def read_partition(self, partition:str) -> pl.LazyFrame:
        try:
            import os
            logger.info(f"Reading partition '{partition}' from layer '{self.layer}'...")
            
            #Confere se o arquivo existe
            if not os.path.exists(f"{self.layer}/{partition}"):
                logger.info(f"Partition '{partition}' was not found in layer '{self.layer}'.")
                return None
            
            df = pl.scan_parquet(
                f"{self.layer}/{partition}/**/*.parquet",
                hive_partitioning=True)
            
            logger.info(f"Partition '{partition}' found and loaded.")
            return df
            
        except Exception as e:
            logger.error(f"Failed to read partition '{partition}' from layer '{self.layer}'.")
            raise ValueError(e)
            
                
            
            
        
            
            
            
                
        
        
            
            
        
    

