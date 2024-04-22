import strawberry
from typing import Optional
from datamanager import DataManager
from datatypes import *
from resolvers import Resolvers
from pagination import PaginationWindow
from enums import CampoFiltro, CampoFiltroDetalle

# Tipos del sistema
@strawberry.type
class Query:
    @strawberry.field(description="Devuelve una lista de datos basicos de clientes")
    def clientes(self, limit: int = 20, offset: int = 0, campo: Optional[CampoFiltro] = strawberry.UNSET, 
                 valores: Optional[str] = strawberry.UNSET) -> PaginationWindow[Cliente]:
        return Resolvers.getClientes(limit, offset, campo, valores)
        
    @strawberry.field
    def cliente(self, llaveMDM: str) -> Cliente | None:
        return Resolvers.getCliente(llaveMDM)

    @strawberry.field(description="Devuelve una lista de detalles de clientes")
    def detalle_clientes(self, limit: int = 5, offset: int = 0,
                         campo: Optional[CampoFiltroDetalle] = strawberry.UNSET, 
                        valores: Optional[str] = strawberry.UNSET) -> PaginationWindow[DetalleCliente]:
        return Resolvers.getDetallesClientes(limit, offset, campo, valores)