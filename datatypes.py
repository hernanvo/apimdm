from ast import List
from typing import Dict, Any, Optional
import typing
import strawberry
from random import seed
from random import randint
import config

# datos detallados cliente
@strawberry.type
class Contacto:
    llaveMDM: str = strawberry.field(description="Identificador asignado al cliente.")
    nombre: str = strawberry.field(description="Nombre completo del contacto")
    celular: str = strawberry.field(description="Nro. celular")
    email: str = strawberry.field(description="direccion de correo")
    direccion: str = strawberry.field(description="direccion")
    ciudad: str = strawberry.field(description="ciudad")

    def getContactosCliente(root):
        cantidad = randint(0,12)
        contactos = []

        if cantidad >= 1:
            contactos.append(Contacto(llaveMDM = root.llaveMDM, nombre="nombre contacto 1", celular="3144142233", email="nnnn@dummy.com",
                                    direccion="Calle 13 # 45-78", ciudad="Medellín"))
        
        if cantidad >= 5:
            contactos.append(Contacto(llaveMDM = root.llaveMDM, nombre="nombre contacto 2", celular="3182165599", email="correo@dominio.com",
                                    direccion="Av Colon # 87-23", ciudad="Bogotá"))
        if cantidad >= 9:
            contactos.append(Contacto(llaveMDM = root.llaveMDM, nombre="nombre contacto 3", celular="3176543210", email="jperez@test.com",
                                    direccion="Cra 38 # 135-23", ciudad="Bogotá"))

        return contactos

# datos detallados cliente
@strawberry.type
class DetalleCliente:
    llaveMDM: str = strawberry.field(description="Identificador asignado al cliente.")
    primerNombre: str = strawberry.field(description="Tipo de documento del cliente")
    segundoNombre: str = strawberry.field(description="Número de documento del cliente.")
    primerApellido: str = strawberry.field(description="Tipo y número de documento del cliente.")
    segundoApellido: str = strawberry.field(description="Segundo Apellido.")
    nombre: str = strawberry.field(description="Nombre empresa o PN.")
    genero: str = strawberry.field(description="M o F.")
    estadoCivil: str = strawberry.field(description="Aplica a PN.")
    
    def getDetalleCliente(root):
        detalleCliente = None

        for item_detail in config.listaClientes:
            if item_detail["llaveMDM"] == root.llaveMDM:
                detalleCliente = DetalleCliente(llaveMDM=item_detail["llaveMDM"],
                                                primerNombre=item_detail["primerNombre"],
                                                segundoNombre=item_detail["segundoNombre"],
                                                primerApellido=item_detail["primerApellido"],
                                                segundoApellido=item_detail["segundoApellido"],
                                                nombre=item_detail["nombre"],
                                                genero=item_detail["genero"],
                                                estadoCivil=item_detail["estadoCivil"])
                break

        return detalleCliente

    @staticmethod
    def from_row(row: Dict[str, Any]):
        return DetalleCliente(llaveMDM=row["llaveMDM"], primerNombre=row["primerNombre"], 
                              segundoNombre=row["segundoNombre"], primerApellido=row["primerApellido"], 
                              segundoApellido=row["segundoApellido"], nombre=row["nombre"],
                              genero=row["genero"], estadoCivil=row["estadoCivil"])

# Datos basicos Cliente MDM
@strawberry.type
class Cliente:
    llaveMDM: str = strawberry.field(description="Identificador asignado al cliente.")
    tipoId: str = strawberry.field(description="Tipo de documento del cliente")
    numeroId: str = strawberry.field(description="Número de documento del cliente.")
    tipoPersona: str = strawberry.field(description="Persona natural o jurídica.")
    nombre: str = strawberry.field(description="Nombres y apellidos del cliente.")
    detalle: Optional[DetalleCliente] = strawberry.field(resolver=DetalleCliente.getDetalleCliente)
    contactos: typing.List["Contacto"] = strawberry.field(resolver=Contacto.getContactosCliente)

    @strawberry.field
    def documento(self) -> str:
        return f"{self.tipoId}!{self.numeroId}"

    @staticmethod
    def from_row(row: Dict[str, Any]):
        return Cliente(llaveMDM=row["llaveMDM"], tipoId=row["tipoId"], numeroId=row["numeroId"], 
                       tipoPersona=row["tipoPersona"], nombre=row["nombre"])
