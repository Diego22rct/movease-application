import json
from pydantic import BaseModel


class IncidentResource(BaseModel):
    title: str
    description: str
    status: str
    images: list[str] = []


class Incident(IncidentResource):
    id: int
    created_at: str
    updated_at: str

    @classmethod
    def model_load(cls, json_data):
        return cls(**json.loads(json_data))
