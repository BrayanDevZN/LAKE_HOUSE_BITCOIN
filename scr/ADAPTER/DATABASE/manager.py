
#Controla as camadas

from scr.ADAPTER.DATABASE.control_json import ControlJson
from scr.ADAPTER.DATABASE.control_parquet import ControlParquet
from typing import Literal

#Controla as camadas
class Layer:
    def __init__(self, layer:Literal["raw", "processed", "cleaned"])->None:
        self.layer = layer
        
        self.instance = self.Get()
      
    #Decide qual classe de controle de arquivo usar  
    def Get(self)  -> ControlJson | ControlParquet:
        if self.layer == "raw":
            instance = ControlJson()
            
            
        elif self.layer == "processed":
            instance = ControlParquet(layer="ADAPTER/STORAGE/PROCESSED")
            
        else: 
            instance = ControlParquet(layer="ADAPTER/STORAGE/CLEANED")
            
        return instance
    
    #Le o arquivo na camada
    def read(self):
        return self.instance.read()
    
    #salva o arquivo na camada
    def save(self, data):
        return self.instance.save(data=data)
    
    #Salva os dados particionados na camada PROCESSED
    def partition(self, data, column):
        if self.layer == "processed":
            return self.instance.partition(data=data, column=column)
        
        raise ValueError(f"Not method in layer {self.layer}")
    
    #Le o arquivo la camada PROCESSED
    def read_partition(self, partition):
        if self.layer == "processed":
            return self.instance.read_partition(partition=partition)
        
        raise ValueError(f"Not method in layer {self.layer}")
        
    
    

    
    
    
    
        





