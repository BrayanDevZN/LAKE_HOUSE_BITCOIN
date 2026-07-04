#Pega os logs
from scr.LOGS import global_logs
import logging

logger = logging.getLogger(__name__)

#salva os arquivos em json em storage e le
import json

class ControlJson:
    
        
    def save(self, data:dict) -> bool:
        try:
            logger.info("Saving API response data to the raw layer...")
            
            with open(f"ADAPTER/STORAGE/RAW/data", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            logger.info("Raw-layer data saved successfully.")
            return True
            
        except Exception as e:
            logger.error("Failed to save the raw-layer file.")
            raise ValueError(e)
            
        
    def read(self) -> dict|None:
        
        try:
            logger.info("Reading data from the raw layer...")
            
            with open("ADAPTER/STORAGE/RAW/data", "r") as f:
                data = json.load(f)
                
            logger.info("Raw-layer file read successfully.")
            return data
        
        except FileNotFoundError:
            logger.warning("Raw-layer file was not found.")
            return None
        
        except Exception as e:
            logger.error("Failed to read the raw-layer file.")
            
            raise ValueError(e)
        
        
        
    
            
                
        
        
