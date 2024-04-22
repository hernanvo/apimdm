import typing
import strawberry
from typing import Optional
import config
from pagination import Pagination, PaginationWindow
from enums import CampoFiltro, CampoFiltroDetalle
from datatypes import Cliente, DetalleCliente


class Resolvers:
    @staticmethod
    def getClientes(limit: int, offset: int, campo: Optional[CampoFiltro] = strawberry.UNSET, 
                    valores: Optional[str] = strawberry.UNSET) -> PaginationWindow[Cliente]:
        filters = {}
        
        if campo != strawberry.UNSET and valores != strawberry.UNSET:
                filters[campo.value] = valores
                
        return Pagination.get_pagination_window(dataset=config.listaClientes, 
                                                ItemType=Cliente,
                                                order_by="llaveMDM",
                                                limit=limit,
                                                offset=offset,
                                                filters=filters)
        

    @staticmethod
    def getDetallesClientes(limit: int = 2, offset: int = 0, 
                            campo: Optional[CampoFiltroDetalle] = strawberry.UNSET, 
                            valores: Optional[str] = strawberry.UNSET) -> PaginationWindow[DetalleCliente]:
        filters = {}
        
        if campo != strawberry.UNSET and valores != strawberry.UNSET:
                filters[campo.value] = valores
                
        return Pagination.get_pagination_window(dataset=config.listaClientes, 
                                                ItemType=DetalleCliente,
                                                order_by="llaveMDM",
                                                limit=limit,
                                                offset=offset,
                                                filters=filters)      

    @staticmethod
    def getCliente(llaveMD: str) -> Cliente | None:
        cliente_data = next((x for x in config.listaClientes if x.llaveMDM == llaveMD), None )
        if cliente_data != None:       
            return Cliente(llaveMDM=cliente_data.llaveMDM, tipoId=cliente_data.tipoId, 
                           numeroId=cliente_data.numeroId, tipoPersona=cliente_data.tipoPersona, 
                           nombre=cliente_data.nombre)
        else:
            return None