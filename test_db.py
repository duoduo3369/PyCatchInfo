#!/user/bin/python
#! -*- encoding:utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import *

engine = create_engine("mysql://root:duoduo@localhost:3306/test?charset=utf8",encoding = "utf-8",echo=True)

metadata = MetaData()

title = Table('hdoj',metadata,
		Column('title',String,nullable=False),
		)

users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(20)),
    Column('fullname', String(20)),
    Column('password', String(20)),
#    mysql_engine='InnoDB'
)

metadata.create_all(engine)

class User(object):
    def __init__(self,name,fullname,password):
        self.name=name
        self.fullname=fullname
        self.password=password

    def __repr__(self):
        return "<User('%s','%s','%s')>" % (self.name,self.fullname,self.password) 

mapper(User,users_table)

Session = sessionmaker(bind=engine)

sess = Session()

ed_user = User('ed', 'Ed Jones', 'edspassword')
sess.add(ed_user)
our_user = sess.query(User).filter_by(name='ed').first()
sess.add_all([
	User('wendy', 'Wendy Williams', 'foobar'),
	User('mary', 'Mary Contrary', 'xxg527'),])
