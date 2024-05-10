from pydantic import BaseModel, Field


class DogBreedRequest(BaseModel):
    number: int = Field(gt=0, lt=9)