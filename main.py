from fastapi import FastAPI
from typing import List, TypeVar, Dict, Any, Generic, Optional
import strawberry
from strawberry.asgi import GraphQL
from strawberry.fastapi import GraphQLRouter
from datamanager import DataManager
from apischema import Query
import os
import requests
from jose import jwt, jwk
from jose.utils import base64url_decode

JWK = Dict[str, str]
JWKS = Dict[str, List[JWK]]
 
def get_hmac_key(token: str, jwks: JWKS) -> Optional[JWK]:
    kid = jwt.get_unverified_header(token).get("kid")
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key

def get_decoded_jwt(token: str, jwks: JWKS) -> bool:
    hmac_key = get_hmac_key(token, jwks)

  if not hmac_key:
        raise ValueError("No pubic key found!")

    hmac_key = jwk.construct(get_hmac_key(token, jwks))

    message, encoded_signature = token.rsplit(".", 1)
    decoded_signature = base64url_decode(encoded_signature.encode())
    return decoded_signature
  
async def get_current_service(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
  
    decoded_token = get_decoded_jwt(token, jwks)
    if not hmac_key.verify(message.encode(), decoded_signature):
      raise credentials_exception
      
    return decoded_token

async def get_context(request: Request):
    service = await get_current_service(request.headers.get("Authorization"))
    return {"service": service}

# startup
DataManager.LoadData()

schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

