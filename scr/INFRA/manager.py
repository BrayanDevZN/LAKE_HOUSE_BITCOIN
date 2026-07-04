from scr.INFRA.CORE.setting import Settings

#Pega a url nas variaveis de ambiente, depois faz a requisição pra ela
from scr.INFRA.CONNECT.request import Request

class RequestData:
    def __init__(self)->None:
        self.__url = Settings.url
        
    def Get(self) -> None | dict:
        response = Request(url=self.__url)
        return response
    
    
#Pega a url do Redis no env e faz conexão com Celery
from scr.INFRA.CONNECT.connect import engine
from celery import Celery

class Engine:
    def __init__(self)->None:
        self.__broker= Settings.broker
        self.__backend = Settings.backend
        
    def Con(self) -> Celery:
        return engine(broker=self.__broker, backend=self.__backend)()
    
    
#Instancia do redis
app = Engine().Con()
  


