# administrador de acceso a datos
from typing import List
import json
import config

#dataset de clientes    

class DataManager():
    @staticmethod
    def LoadData():
        print("LoadData")

        with open('data\\testdata.json') as json_file:
            dataClientes = json.load(json_file) 
            config.listaClientes = dataClientes['data'].copy()

        for item in config.listaClientes:
            item["documento"] = f"{item['tipoId']}!{item['numeroId']}"
            item["nombre"] = f"{item['primerNombre']} {item['segundoNombre']}. {item['primerApellido']} {item['segundoApellido']}"

