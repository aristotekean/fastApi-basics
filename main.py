# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, EmailStr, Field

# FastAPI
from fastapi import (Cookie, FastAPI, File, UploadFile, status,
                     Header, Body, Query, Path, Form, HTTPException)

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


@app.get(path="/", status_code=status.HTTP_200_OK, tags=["Home"], summary="Hello world")
def home():
    """Hello world

    This path operation start the app

    Args:

    Returns:
    - The following dic "{"hello": "world"}"
    """
    return {"hello": "world"}

# Request and Response Body


@app.post(path="/person/new", response_model=PersonOut, status_code=status.HTTP_201_CREATED, tags=["Persons"], summary="Create Person in the app")
def create_person(person: Person = Body(...)):
    """Create Person

    This path operation creates a person in the app and save the information in the database

    Args:
    - Request body parameter:
        - **person: Person** -> A person model with first name, last name, age, hair color and marital status

    Returns:
    - A person model with first name, last name, age, hair color and marital status
    """
    return person

# Validations query parameters


@app.get(path="/person/detail", status_code=status.HTTP_200_OK, tags=["Persons"], summary="Get Person detail", deprecated=True)
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
    """Get person detail

    Args:    
    - Request query parameter:
        name (Optional[str], optional): _description_. Defaults to Query( None, min_length=1, max_length=50, title="Person Name", description="This is the person name. It's between 1 and 50 characters", example="kevin" ).
        age (str, optional): _description_. Defaults to Query( ..., title="Person Age", description="This is the person name. It's required", example=33 ).

    Returns:
        A dic with name and age
    """
    return {name: age}


# validations path parameters

persons = [1, 2, 3, 4, 5]


@app.get(path="/person/detail/{person_id}", status_code=status.HTTP_200_OK, tags=["Persons"], summary="Get a person")
def show_person(
        person_id: int = Path(
            ...,
            title="Person id",
            description="This is the person id. It's required and greate than 1",
            gt=0,
            example=43
        )):
    """Show a Person by ID

    Args:
        person_id (int, optional): _description_. Defaults to Path( ..., title="Person id", description="This is the person id. It's required and greate than 1", gt=0, example=43 ).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person does not exist"
        )
    return {person_id: "It exists!"}

# validations request body


@app.put(path="/person/{peson_id}", status_code=status.HTTP_200_OK, tags=["Persons"], summary="Update person")
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
    """Update a Person by ID

    Args:
        person_id (int, optional): _description_. Defaults to Path( ..., title="Person id", description="This is the person id. It's required and greate than 1", gt=0, example=43 ).
        person (Person, optional): _description_. Defaults to Body( ... ).

    Returns:
        _type_: _description_
    """
    # results = person.dict()
    # results.update(location.dic)
    # return results
    return person

# Form


@app.post(path="/login", response_model=LoginOut, status_code=status.HTTP_200_OK, tags=["Persons"], summary="Signin")
def login(username: str = Form(...), password: str = Form(...)):
    """Start the sesion

    Args:
        username (str, optional): _description_. Defaults to Form(...).
        password (str, optional): _description_. Defaults to Form(...).

    Returns:
        _type_: _description_
    """
    return LoginOut(username=username)

# Cookies and headers parameters


@app.post(path="/contact", status_code=status.HTTP_200_OK, tags=["Home"])
def contact(first_name: str = Form(..., max_length=20, min_length=1),
            last_name: str = Form(..., max_length=20, min_length=1),
            email: EmailStr = Form(...),
            message: str = Form(..., min_length=20),
            user_agent: Optional[str] = Header(default=None),
            ads: Optional[str] = Cookie(default=None),
            summary="get in touch"
            ):
    """_summary_

    Args:
        first_name (str, optional): _description_. Defaults to Form(..., max_length=20, min_length=1).
        last_name (str, optional): _description_. Defaults to Form(..., max_length=20, min_length=1).
        email (EmailStr, optional): _description_. Defaults to Form(...).
        message (str, optional): _description_. Defaults to Form(..., min_length=20).
        user_agent (Optional[str], optional): _description_. Defaults to Header(default=None).
        ads (Optional[str], optional): _description_. Defaults to Cookie(default=None).
        summary (str, optional): _description_. Defaults to "get in touch".

    Returns:
        _type_: _description_
    """
    return user_agent


# Files

@app.post(path="/post-image", status_code=status.HTTP_200_OK, tags=["Posts"], summary="Upload post-image")
def post_image(image: UploadFile = File(...)):
    """_summary_

    Args:
        image (UploadFile, optional): _description_. Defaults to File(...).

    Returns:
        _type_: _description_
    """
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }
