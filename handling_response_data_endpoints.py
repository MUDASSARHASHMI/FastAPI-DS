from pathlib import Path
from fastapi import FastAPI, status, Body, HTTPException
from fastapi.openapi.models import Response
from pydantic import BaseModel
from pydantic.v1 import root_validator
from starlette.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.responses import FileResponse
"""Most of the time FastAPI will return status_code 200 but its good
to have 201 once an object is created.
"""
# class Post(BaseModel):
#     title: str
#     nb_views: int
app = FastAPI()
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# async def create_post(post: Post):
#     return post
# Dummy database object
# posts = {
#     1: Post(title="Hello World", nb_views=100),
# }
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id: int):
#     posts.pop(id, None)
#     return None

# The response Model
"""Usually a JSON object is returned for the request but sometimes
we see that the data we saved and data we want end user to see is
quite different or perhaps some fields are only useful during the 
creation process and then discarded afterwards."""
# class PublicPosts(BaseModel):
#     title: str
# @app.get("/post/{id}")
# async def get_post_id(id: int):
#     return posts
# @app.get("/poster/{id}", response_model=PublicPosts)
# async def get_poster_id(id: int):
#     return posts[id]
# Setting custom headers
"""Its useful to sometimes return custom headers as response."""
# @app.get("/")
# async def custom_header(response: Response):
#     response.headers["Custom-Header"] = "Custom-Header-Value"
#     return {"hello": "world"}
# Set Cookies
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def set_cookies(response: Response):
    response = JSONResponse(content={"Hello": "World"})
    response.set_cookie(
        key="cookie-name",
        value="cookie-value",
        max_age=86400,      # 24 hours

    )
    return response
"""This is how we can set cookies for the API and or we can also
get the cookies already available in the browser."""

# Setting the status code Dynamically
"""Assume that we have an endpoint that needs to return dynamic
result like 200 for success 201 to create the object if doesn't
exist. So dynamic means it responds as per situation."""
#Dummy Database
class Post(BaseModel):
    title: str
posts = {
    1: Post(title="Hello")
}
@app.put("/posts/{id}")
async def udpate_or_create_post(id: int, post: Post, response: Response):
    if id not in posts:
        response.status_code = status.HTTP_201_CREATED
    posts[id] = post
    return posts[id]
# So simple if condition will result 201 otherwise it will show 200

#Raising HTTP Error codes with FastAPI
"""Two very important ways to produce errors in FastAPI are payloads
and status codes. In FastAPI we can also raise Python exception
HTTPException and it allows us to set status code errors."""
# Raising 400 if Password and Password Confirm properties don't
# Match
@app.post("/password")
async def check_password(password: str=Body(...), password_confirm: str=Body(...)):
    if password != password_confirm:
        # raise HTTPException(
        #     status.HTTP_400_BAD_REQUEST,
        #     detail="Password don't match."
        # )
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Password don't match.",
                "Hint": ["Check the CAPS lock on the Keyboard.",
                         "Try to make the password visible by clicking on the eye icon to check your typing",
                        ],

            },
        )
    return {"message": "Password Match"}
# Run below command to test it in terminal
#http POST http://localhost:8000/password password="aa" password_confirm="bb"

#Building a custom response
"""Type of custom responses include:
    - HTML Response: Returns HTML
    - Plain text response: Returns text response 
    - Redirect Response: Can redirect to another response
    - Streaming Response: Streams the flow of bytes
    - File response: Returns the response with a file
"""
# Using the response_class argument
# This will be suited for HTMLResponse and PlainTextResponse
@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return """
    <html>
    <head>
    <title> This is the title. </title> 
    </head>
    <body><h1>This is the body </h1></body>
    </html>
    """
@app.get("/text", response_class=PlainTextResponse)
async def get_text():
    return "Hello World"
# By setting "response_class" argument on decorator, we can change
# the class FastAPI will use to build the response.
"""The nice thing is that we can combine this option with the ones
we saw in Path operation parameter section"""
# Making Redirections
@app.get("/redirect")
async def redirect():
    return RedirectResponse("/text")
"""Default redirect code is 307 but we can change it using Redirect
with status_code argument."""
@app.get("/redirected")
async def change_redirect_status():
    return RedirectResponse("/text", status_code=status.HTTP_301_MOVED_PERMANENTLY)

# Serving a file
@app.get("/cat")
async def get_cat():

    root_directory = Path(__file__).parent
    picture_path = root_directory/"cat.jpg"
    return FileResponse(picture_path)
# Get XML response
@app.get("/xml")
async def get_xml():
    content = """<?xml version="1.0" encoding="UTF-8"?>
    <Hello>World</Hello>
    """
    return Response(content=content, media_type="application/xml")