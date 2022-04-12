# import jwt
from asyncore import write
from math import prod
# import os,uuid,aiofiles,shutil

from fastapi import APIRouter,Response,UploadFile,File,Depends,HTTPException,status,Form
# from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import List,Callable
# from pathlib import Path
from tempfile import NamedTemporaryFile
# from jose import JWTError, jwt
from passlib.hash import bcrypt
from passlib.context import CryptContext
from pydantic import EmailStr
from config.db import conn
from models.user import users,products
from schemas.user import Login, User,Product
from sqlalchemy.sql import text
from starlette.status import HTTP_204_NO_CONTENT

# from fastapi.responses import FileResponse
import uuid
from fastapi.responses import FileResponse
import os
from random import randint
import uuid

IMAGEDIR_PRODUCT = "images/Products/"
IMAGEDIR_USER = "images/Users/"

from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

router = APIRouter()

# oauth2_sheme = OAuth2PasswordBearer(tokenUrl='token')

# @router.get('/')
# def tok_token(token: str = Depends(oauth2_sheme)):
#     return {'the_token ' : token}
 

# async def authenticate_user(email :EmailStr, password: str):
#     log = await Login.get(email=email) 
#     if not log:
#         return False
#     if not log.verify_password(password):
#         return False
#     return log

# @router.post('/token')
# async def generate_token(token_data: OAuth2PasswordRequestForm = Depends()):
#     log = await authenticate_user(token_data.email, token_data.password)
    
#     if not log :
#         return {'error':'Invalid Credentials'}
#     user_obj = await User
    
#     # return {'access_token' : token_data.password + 'token'}


#-----------------------------          Login Page        ---------------------------------------------------------------------------------------------------------------------------


@router.post("/login")
def login_user(user:User):
    # log_user = {
    #     "password":user.password
    # }
    
    s = text("select users.email, users.password from users where users.email = :x and users.password = :y")
    
    result = conn.execute(s, x = user.email , y = user.password).fetchall()
    if result:
        return "Login Successful"
    
    else:
        return "Incorrect Email or password!"
  


#-----------------------------          Signup Page        ---------------------------------------------------------------------------------------------------------------------------

###########      Read all datas      #############

@router.get("/signup")
def read_user(): 
    return conn.execute(users.select()).fetchall()

############    Read datas with id       ###########

@router.get("/signup/{id}")
def read_user(id):
    return conn.execute(users.select().where(users.c.id == id)).fetchall()


############      Create data    ###########

@router.post("/signup")
async def create_user(user:User = Depends(),file:UploadFile =File(...)):
    
    new_user = {
        "name":user.name,
        "email":user.email,
        "user_img":file.filename,
        "password":user.password
        }
    
    # Store User Images Locally on Images/Users
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()  # <-- Important!

    # example of how you can save the file
    with open(f"{IMAGEDIR_USER}{file.filename}", "wb") as f:
        f.write(contents)

    
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()
   

############        Delete data     ###########

@router.delete("/signup/{id}")
def delete_user(id):
    conn.execute(users.delete().where(users.c.id == id))
    return "Data deleted"
    # return Response(status_code=HTTP_204_NO_CONTENT)


############        Update data     ###########

@router.put("/signup/{id}")
def update_user(id,user:User = Depends(),file:UploadFile=File(...)):
    conn.execute(users.update().values(name=user.name,email=user.email,password=user.password,user_img=file.filename).where(users.c.id == id))
    # return "Data Updated"
    return conn.execute(users.select().where(users.c.id == id)).first()


#-----------------------------          Profile Page        ---------------------------------------------------------------------------------------------------------------------------

# ############    Read datas with id       ###########

@router.get("/profile/{id}")
def read_profile(id):

    s = text("select users.name, users.email, users.user_img from users where users.id = :x ")
    result = conn.execute(s, x = id).fetchall()
    if result:
        return result
    else:
        return "User Not Exists"


#-----------------------------          Product Page        ---------------------------------------------------------------------------------------------------------------------------


###########      Read all datas      #############

@router.get("/products")
def read_product(): 
    return conn.execute(products.select()).fetchall()


# ############    Read datas with id       ###########

@router.get("/products/{id}")
def read_product(id):
    return conn.execute(products.select().where(products.c.id == id)).fetchall()


############      Create data    ##########

@router.post("/products")
async def create_product(product:Product = Depends(),file:UploadFile = File(...)):
    new_product = {
        "product_image":file.filename,
        "product_name":product.product_name,
        "price":product.price,
        "description":product.description
        } 

    # store user datas loacally on Images/Products 
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()  # <-- Important!
    
    # example of how you can save the file
    with open(f"{IMAGEDIR_PRODUCT}{file.filename}", "wb") as f:
        f.write(contents)
        
       
    result_product = conn.execute(products.insert().values(new_product))
    return conn.execute(products.select().where(products.c.id == result_product.lastrowid)).first()
   

############        Delete data     ###########

@router.delete("/products/{id}")
def delete_product(id):
    conn.execute(products.delete().where(products.c.id == id))
    return "Data deleted"
    # return Response(status_code=HTTP_204_NO_CONTENT)


############        Update data     ###########

@router.put("/products/{id}")
def update_product(id,product:Product = Depends(),file:UploadFile = File(...)):
    conn.execute(products.update().values(product_name=product.product_name,price=product.price,description=product.description,product_image=file.filename).where(products.c.id == id))
    # return "Data Updated"
    return conn.execute(products.select().where(products.c.id == id)).first()


# # Get Image by view
# @router.get("/images/{id}")
# async def read_random_file():

#     # get a random file from the image directory
#     files = os.listdir(IMAGEDIR_PRODUCT)
#     random_index = randint(0, len(files) - 1)

#     path = f"{IMAGEDIR_PRODUCT}{files[random_index]}"
    
#     # notice you can use FileResponse now because it expects a path
#     return FileResponse(path)
