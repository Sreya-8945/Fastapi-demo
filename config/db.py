from sqlalchemy import create_engine,MetaData
# from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql+pymysql://root:@localhost:3306/apidb")
# engine = create_engine("mysql+pymysql://--host=localhost --user=myname --password")
# engine = create_engine("mysql+pymysql://{username}:{password}@localhost:3306/apidb".format(username,password))
meta = MetaData()
conn = engine.connect()
