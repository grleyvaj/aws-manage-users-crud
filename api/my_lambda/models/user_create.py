from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    last_name: str = Field(min_length=2, max_length=30)
    charge: str = Field(min_length=2, max_length=30)
    email: str = Field(regex=r'^[\w\.-]+@[\w\.-]+$')
