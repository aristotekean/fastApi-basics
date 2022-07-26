# Python
from doctest import Example
from email import message
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, EmailStr, Field

# FastAPI
from fastapi import Cookie, FastAPI, status, Header, Body, Query, Path, Form

app = FastAPI()

# Models


class HairColor(str, Enum):
    white = "white"
    blonde = "blonde"
    brown = "brown"
    black = "black"


class PersonBase(BaseModel):
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


class Person(PersonBase):

    password: str = Field(..., min_length=8)

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


class PersonOut(PersonBase):
    pass


class Location(BaseModel):
    city: str = Field(..., min_length=1, max_length=150)
    state: str = Field(..., min_length=1, max_length=150)
    country: str = Field(..., min_length=1, max_length=100)


class LoginOut(BaseModel):
    username: str = Field(..., min_length=1, max_length=10, example="valeryok")
    message: str = Field(default="Login successfully")


@app.get(path="/", status_code=status.HTTP_200_OK)
def home():
    return {"hello": "world"}

# Request and Response Body


@app.post(path="/person/new", response_model=PersonOut, status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)):
    return person

# Validations query parameters


@app.get(path="/person/detail", status_code=status.HTTP_200_OK)
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


@app.get(path="/person/detail/{person_id}", status_code=status.HTTP_200_OK)
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


@app.put(path="/person/{peson_id}", status_code=status.HTTP_200_OK)
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

# Form


@app.post(path="/login", response_model=LoginOut, status_code=status.HTTP_200_OK)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

# Cookies and headers parameters


@app.post(path="/contact", status_code=status.HTTP_200_OK)
def contact(first_name: str = Form(..., max_length=20, min_length=1),
            last_name: str = Form(..., max_length=20, min_length=1),
            email: EmailStr = Form(...),
            message: str = Form(..., min_length=20),
            user_agent: Optional[str] = Header(default=None),
            ads: Optional[str] = Cookie(default=None)
            ):
    return user_agent
