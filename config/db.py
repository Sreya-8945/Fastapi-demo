from sqlalchemy import create_engine,MetaData
# from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql+pymysql://root:@localhost:3306/apidb")
meta = MetaData()
conn = engine.connect()


# mw = sessionmaker(bind=engine)
# session = Session()