from __future__ import annotations
from pydantic import BaseModel


class ResourceDeleteRequest(BaseModel):
    resource_id: str


class LLMResourcesRequest(BaseModel):
    model: str
    gpu_resource: GpuResource


class EmptyResourcesRequest(BaseModel):
    cpu: str
    memory: str


class PrivateEmptyResource(BaseModel):
    cpu: str
    memory: str
    resource_id: str
    host: str
    password: str
    port: int
    username: str = "root"


class PrivateLLMResource(BaseModel):
    model: str
    resource_id: str
    gpu_resource: GpuResource


class GpuResource(BaseModel):
    resource_id: str | None = None
    gpu_type: str
    gpu_count: int
    description: str | None = None
