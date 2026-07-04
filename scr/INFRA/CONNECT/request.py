
#Pega a configuração de logs
import logging
from scr.LOGS import global_logs

logger = logging.getLogger(__name__)


#Faz a requisição pra api externa
import requests
def Request(url:str) -> dict|None:
    
    logger.info("Sending request to the external data source...")
    response = requests.get(url=url)
    
    if response.status_code !=200:
        
        logger.error(f"External data request failed with status {response.status_code}: {response.text}")
        return None
    
    logger.info("External data request completed successfully.")
    
    return response.json()

