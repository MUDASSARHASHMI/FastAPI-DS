from enum import Enum
from fileinput import filename



from fastapi import FastAPI, Path, Query, Body, Form, File, UploadFile, Header, Cookie, Request

from pydantic import BaseModel
app = FastAPI()

class UserType(str, Enum):
    STANDARD = "standard"
    ADMIN = "admin"

@app.get("/")
async def hello_world():
    return {"Hello": "World"}

# Dynamic Parameters for Path

# @app.get("/users/{id}")
# async def get_users(id: int):
#     return {"id": id }

# @app.get("/users/{type}/{id}")
# async def get_user(type: str, id: int):
#     return {"type": type, "id":id}

# Limiting users with Enum

@app.get("/users/{type}/{id}")
async def get_user(type: UserType, id: int):
    return {"type": type, "id": id}

# Advance way to handle the data validation
@app.get("/users/{id}")
async def get_users(id: int = Path(..., ge=1)):
    return {"id": id}
# License Plate number regular expression based on URL (French License Plate)
@app.get("/license-plate/{license}")
async def get_license_plate(license: str = Path(..., min_length=9, max_length=9)):
    return {"license": license}

# Regular expression version of license plate
@app.get("/license-plate/{license-plate}")
async def get_license_plate_re(license_plate: str = Path(..., regex=r"^\w{2}-\d{3}-\w{2}$")):
    return {"license-plate": license_plate}
# r Means raw string in regex
# ^ means start of expression
# \w{2} means 2 words
# \d{3} means 3 digits
# - means another literal
# $ means end of string

# Parameter Metadata
"""Data validation is not only option accepted by the parameter
function. We can also set options that will add information about
the parameter in automatic documentation, such as title, description
and deprecated."""
# Query Parameters
"""Query Parameters are a common way to add some dynamic parameters
to a URL. We can find them at the end of the URL in the following
form '?param1=foo&param2=bar. In rest API they are commonly used 
to read endpoints to apply pagination, a filter, a sorting order, 
or selecting a fields."""
@app.get("/query_users")
async def get_user_query(page: int=1, size: int=10):
    return {"page": page, "size": size}
class UserFormat(str, Enum):
    SHORT = "short"
    LONG = "long"

@app.get("/limit_argument")
async def get_limited_user(format: UserFormat):
    return {"format": format}

# Query Parameter using Query

@app.get("/q-users")
async def q_users(page: int=Query(1, gt=0), size: int=Query(10, le=100)):
    return {"page": page, "size": size}
#Request Body
""" The body is part of HTTP request that contains raw dat representing
documents, files or form submission. In REST API its usually encoded
in JSON and used to create structured objects in database.

For the simplest case, retrieving data from the body works exactly
like query parameter. The only difference is that you always have 
to use the BODY function otherwise FastAPI will look for it inside
the query parameters by default.
"""
@app.post("/users")
async def create_user(name: str= Body(...), age: int=Body(...)):
    return {"name": name, "age": age}
# We can run this function with Httpie installed and with -v option
# So we can see clearly what is being printed in body
# http -v POST http://localhost:8000/users name="John" age=30
"""Defining payloads validation such as this has major drawbacks.
First, its quite verbose and makes the path operations function 
prototype huge, especially for bigger models. Second, usually,
you'll need to reuse the data structure on other endpoints or in 
other parts of the application. This is why we use Pydantic models.
Pydantic is a Python library for data validation and is based on 
classes and type hints. Path, Query and Body we used so far use 
Pydantic under the hood."""
class User(BaseModel):
    name: str
    age: int

@app.post("pydantic-users")
async def create_pydantic_user(user: User):
    return user

# Using Multiple objects
class Company(BaseModel):
    company: str
@app.post("/company-user")
async def create_company_user(user: User, company: Company):
    return {"user": user, "company": company}
# Single body value without any model can be added to API like
@app.post("/single-value-users")
async def single_value_user(user: User, company: Company, priority: int = Body(..., ge=1, le=3)):
    return {"user": user, "company": company, "priority": priority}

# Form data and file uploads with FastAPI
# Uses package python-multipart.
@app.post("/user-form")
async def user_form(name: str = Form(...), age: int = Form(...)):
    return {"name" : name, "age": age }
# To test form data
# http -v --form POST http://localhost:8000/users name=John age=30

# File upload
@app.post("/upload")
async def file_upload(file: bytes = File(...)):
    return {"file_size": len(file)}
# To test upload file endpoint
# http --form POST http://localhost:8000/files file@./assets/cat.jpg
"""This works with small files as these small files will be loaded
in cache but for large files it will run out of cache and it needs
to be redirected to the disk space."""
# Upload file function with proper cache management
@app.post("/file-upload")
async def upload_file(file: UploadFile = File(...)):
    return {"file_name": file.filename,
            "content_type": file.content_type}
# Create an asset folder and run below
# http --form POST http://localhost:8000/files file@./assets/cat.jpg
# Adding multiple files upload with "list" type hinting
@app.post("/multiple-files/")
async def multipl_uploads(files: list[UploadFile] = File(...)):
    return [{"filename": file.filename, "content-type": file.content_type} for file in files]

""" Headers contain all the metadata of a request contained with HTTP
and we need to use these metadata for authentication purpose using 
cookies."""

# Using metadata "Header"
# @app.get("/")
# async def get_header_data(hello: str = Header(...)):
#     return {"hello": hello}
# User Agent calling
@app.get("/user-agent")
async def get_header(user_agent: str = Header(...)):
    return {"user_agent": user_agent}

@app.get("/")
async def get_cookies(hello: str | None = Cookie(None)):
    return {"Hello": hello}
# Request Object
"""Sometimes we need to access raw data associated to an object
and that is possible."""
@app.get("/")
async def get_request_object(request: Request):
    return {"path": request.url.path}
"""Under the hood this is the request object from Starlette library
that provides all core logic for FastAPI. """