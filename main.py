# Python
from typing import Optional
from unittest import result

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models


class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


class Location(BaseModel):
    city: str
    state: str
    country: str


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
            description="This is the person name. It's between 1 and 50 characters"
        ),
        age: str = Query(
            ...,
            title="Person Age",
            description="This is the person name. It's required"
        )):
    return {name: age}

# validations path parameters


@app.get("/person/detail/{person_id}")
def show_person(
        person_id: int = Path(
            ...,
            title="Person id",
            description="This is the person id. It's required and greate than 1",
            gt=0
        )):
    return {person_id: "It exists!"}

# validations request body


@app.put("/person/{peson_id}")
def update_person(
        person_id: int = Path(
            ...,
            title="Person id",
            description="This is the person id. It's required and greate than 1",
            gt=0
        ),
        person: Person = Body(
            ...
        ),
        location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dic)

    return results
