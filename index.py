from fastapi import FastAPI
from routes.user import router

app = FastAPI()

# @app.get("/")
# def read_something():
#     return {"msg":"Hello World"}


app.include_router(router)