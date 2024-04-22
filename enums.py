# Tipos de datos expuestos por el API
from typing import List, TypeVar, Dict, Any, Generic, Optional
import strawberry
from enum import Enum


# Campos permitidos en filtro clientes
@strawberry.enum
class CampoFiltro(Enum):
    LLAVE_MDM = "llaveMDM"
    DOCUMENTO = "documento"

# Campos permitidos en filtro detalle
@strawberry.enum
class CampoFiltroDetalle(Enum):
    LLAVE_MDM = "llaveMDM"