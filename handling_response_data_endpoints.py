"""Most of the time FastAPI will return status_code 200 but its good
to have 201 once an object is created.
"""
from fastapi import FastAPI, status
from pydantic import BaseModel

class Post(BaseModel):
    title: str
app = FastAPI()
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    return post
