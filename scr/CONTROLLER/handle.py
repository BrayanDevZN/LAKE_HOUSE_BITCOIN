

from scr.SERVICE.manager import Query
from typing import Literal
class Handle:
    
    @staticmethod
    def HandleQuery(filter:Literal["year", "month", "day"]= None, field:str = None):
        return Query(
            field=field,
            filter=filter
        ).execute()
        
    
    @staticmethod
    def HandleStatusSave(id:str):
        return Query().status_task(id)
            
        
        
        