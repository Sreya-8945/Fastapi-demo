from pydantic import EmailStr,BaseModel
from sqlalchemy import Table,Column,ForeignKey
from config.db import meta,engine
from sqlalchemy.sql.sqltypes import Integer,String


users = Table(
    'users',meta,
    Column('id',Integer,primary_key=True),
    Column('name',String(255)),
    Column('email',String(255)),
    Column('password',String(255)),
    Column('user_img',String(255))
)

products = Table(
    'products',meta,
    Column('id',Integer,primary_key=True),
    Column('product_image',String(255)),
    Column('product_name',String(255)),
    Column('price',String(50)),
    Column('description',String(255))
)


meta.create_all(engine)