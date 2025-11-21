# Defining Models and their field types with pydantic
# Creating Model variations with class inheritance
# Adding custom data validation with Pydantic
# Working with Pydantic Objects

## Standard field types
from datetime import date
from enum import Enum
from pydantic import BaseModel, ValidationError
class UserProfile(BaseModel):
    nickname: str
    location: str | None = None
    subscribed_newsletter: bool = True
class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NON_BINARY = "NON_BINARY"
class Address(str, Enum):
    street_address: str
    postal_code: str
    city: str
    country: str

class Person(BaseModel):
    first_name = str
    last_name = str
    age: int
    gender: Gender
    birthdate: date
    interests: list[str]
    address: Address

