from enum import Enum
from typing import Optional, List
from uuid import uuid4, UUID

from pydantic import BaseModel


class Role(str, Enum):
    admin = 'admin'
    mod = 'mod'


class Gender(str, Enum):
    male = 'male'
    female = 'female'


class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    gender: Gender
    roles: List[Role]
