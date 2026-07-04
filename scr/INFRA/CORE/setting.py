
#Carrega as variaveis de ambiente
from dotenv import load_dotenv

load_dotenv()

#Pega as variaveis de ambiente
import os

class Settings:
    broker=os.getenv("BROKER")
    backend=os.getenv("BACKEND")
    url=os.getenv("URL")