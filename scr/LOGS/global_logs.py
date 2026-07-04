
#Cria o arquivo onde salva os logs caso não exista
import os

os.makedirs("LOGS", exist_ok=True)

#Faz a configuração global de logs
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", #Formato que o log vai aparecer no terminal
    handlers=[ 
        logging.StreamHandler(),
         logging.FileHandler(
            "scr/LOGS/app.log",
            encoding="utf-8"
        )     
    ]
)

