#! -*- encoding:utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import *

def createSession():
	engine = create_engine("mysql://root:duoduo@localhost:3306/test?charset=utf8",encoding = "utf-8",echo=True)
	
	
	metadata = MetaData()

	hdoj_table = Table('hdoj',metadata,
			Column('id',Integer,primary_key=True),
			Column('title',String,nullable=False),
			)
	
	class Hdoj(object):
		def __init__(self,title):
			self.title = title
		
		def __repr__(self):
			return "<Hdoj('%s')>" % (self,title)
	
	metadata.create_all(engine)
	
	mapper(Hdoj,hdoj_table)
	
	Session = sessionmaker(bind=engine)
	
	session = Session()
	return session
