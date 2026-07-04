
#Cria o variavel pra chamar os logs
from scr.LOGS import global_logs
import logging

logger = logging.getLogger(__name__)

#Cria a engine que conecta com redis
from celery import Celery

class engine:
    def __init__(self, broker: str, backend: str) -> None:
        self.__broker = broker
        self.__backend = backend

    def Con(self) -> Celery:
        logger.info("Initializing Celery connection...")

        con = Celery(
            "Lake_house",
            broker=self.__broker,
            backend=self.__backend,
            include=["SERVICE.task"]
        )

        logger.info(f"Celery broker configured: {'yes' if self.__broker else 'no'}.")
        logger.info(f"Celery result backend configured: {'yes' if self.__backend else 'no'}.")
        logger.info("Celery connection initialized.")

        return con

    def __call__(self) -> Celery:
        return self.Con()
        
