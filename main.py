# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models


class HairColor(str, Enum):
    white = "white"
    blonde = "blonde"
    brown = "brown"
    black = "black"


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="facundo"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="cabrera cabrales"
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=22
    )
    hair_color: Optional[HairColor] = Field(
        default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None, example=False)

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "facundo",
    #             "last_name": "cabrera cabrales",
    #             "age": 21,
    #             "hair_color": "black",
    #             "is_married": False
    #         }
    #     }


class Location(BaseModel):
    city: str = Field(..., min_length=1, max_length=150)
    state: str = Field(..., min_length=1, max_length=150)
    country: str = Field(..., min_length=1, max_length=100)


@app.get("/")
def home():
    return {"hello": "world"}

# Request and Response Body


@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validations query parameters


@app.get("/person/detail")
def show_person(
        name: Optional[str] = Query(
            None,
            min_length=1,
            max_length=50,
            title="Person Name",
            description="This is the person name. It's between 1 and 50 characters",
            example="kevin"
        ),
        age: str = Query(
            ...,
            title="Person Age",
            description="This is the person name. It's required",
            example=33
        )):
    return {name: age}

# validations path parameters


@app.get("/person/detail/{person_id}")
def show_person(
        person_id: int = Path(
            ...,
            title="Person id",
            description="This is the person id. It's required and greate than 1",
            gt=0,
            example=43
        )):
    return {person_id: "It exists!"}

# validations request body


@app.put("/person/{peson_id}")
def update_person(
        person_id: int = Path(
            ...,
            title="Person id",
            description="This is the person id. It's required and greate than 1",
            gt=0,
            example=43
        ),
        person: Person = Body(
            ...
        ),
        # location: Location = Body(...)
):
    # results = person.dict()
    # results.update(location.dic)
    # return results
    return person
