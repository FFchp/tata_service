from fastapi import FastAPI
import models, user, billet
from database import engine

# create app for start api
app = FastAPI()

# create database on database platform
models.Base.metadata.create_all(engine)

app.include_router(user.router)
app.include_router(billet.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello")
async def hello():
    return {"msg": "Hello"}


