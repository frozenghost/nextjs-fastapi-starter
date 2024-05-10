from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class CommonResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    success: bool = True
    error: Optional[str] = None

    class Config:
        arbitrary_types_allowed=True

class StaticString:
    DOG_IMAGE_SOURCE = "https://dog.ceo/api/breeds/image/random"