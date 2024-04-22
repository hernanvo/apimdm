from fastapi import FastAPI
from typing import List, TypeVar,Dict, Any, Generic
import strawberry
from strawberry.asgi import GraphQL
from strawberry.fastapi import GraphQLRouter
from datamanager import DataManager
from apischema import Query

# startup
DataManager.LoadData()

schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

