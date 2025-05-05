from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://root:root@localhost:3306/tianc6db',echo=True)
Base = declarative_base()

class Paper(Base):
    __tablename__ = 'papers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    paper_name = Column(String(255), primary_key=True)
    paper_author = Column(String(255))
    paper_date = Column(String(255))
    paper_source = Column(String(255))
    paper_data = Column(String(255))

# 创建表结构（如果不存在）
Base.metadata.create_all(engine)

# 创建会话工厂
Session = sessionmaker(bind=engine)


