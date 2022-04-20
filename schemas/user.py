from pydantic import BaseModel, EmailStr,HttpUrl
from typing import Optional
# from passlib.hash import bcrypt


class Login(BaseModel):
    email:EmailStr
    password:str
     
class User(Login):
    name:str    
    
class ProductImage(BaseModel):
    product_id:int
    product_name:str
    
 
class Product(BaseModel):
    product_name:str
    price:float
    description:str

