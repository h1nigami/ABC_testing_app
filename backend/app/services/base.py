from typing import TypeVar, Generic

RepoType = TypeVar("RepoType")
SchemaRequestType = TypeVar("SchemaRequestType")
SchemaResponseType = TypeVar("SchemaResponseType")

class BaseService(Generic[RepoType, SchemaRequestType, SchemaResponseType]):
    pass