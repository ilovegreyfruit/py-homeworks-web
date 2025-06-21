from pydantic import BaseModel


class AdCreateSchema(BaseModel):
    title: str
    description: str
    owner: str