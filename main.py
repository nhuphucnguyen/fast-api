from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional 
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_post = [{"id": 1, "title": "T 1", "content": "C1"}, {"id": 2, "title": "T2", "content": "C2"}]

def find_post_by_id(id):
    for p in my_post:
        if p['id'] == id:
            return p

@app.get("/posts")
def root():
    return {"data": my_post}

@app.get("/posts/{id}")
def get_post_by_id(id: int, response: Response):
    post = find_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id {id} not found"}
    return post


@app.post("/post")
def create_post(post: Post):
    new_post_dict = post.dict()
    new_post_dict['id'] = randrange(0, 1000000)
    my_post.append(new_post_dict)
    return {"new_post": post}
