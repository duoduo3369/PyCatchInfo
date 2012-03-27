#! -*- encoding:utf-8 -*-
import urllib2
import traceback
from BeautifulSoup import BeautifulSoup
from sqlalchemy import *
from sqlalchemy.orm import *

def catch(url=None):
	content_stream = urllib2.urlopen(url)
	content = content_stream.read()
	print 'catching: ' + url
	soup = BeautifulSoup(content)
	table = soup.table
	#title
	table_title = table.find('h1')
	table_title.hidden = True
	#title below limits description
	table_limit_des = table_title.findNext('span')
	table_limit_des.hidden = True
	# problem description, input, output, sample input, sample output
	try:
		table_problem_des = table.find(text='Problem Description').findNext('div', {'class':'panel_content'})
		table_problem_des.hidden = True
	except Exception as e:
		table_problem_des = None

	#input
	try:
		table_input = table.find(text='Input').findNext('div', {'class':'panel_content'})
		table_input.hidden = True
	except Exception as e:
		table_input = None
	#output
	try:
		table_output = table.find(text='Output').findNext('div', {'class':'panel_content'})
		table_output.hidden = True
	except Exception as e:
		table_output = None
	#sample input
	try:
		table_sample_input = table.find(text='Sample Input').findNext('div', {'class':'panel_content'})
		table_sample_input.hidden = True
	except Exception as e:
		table_sample_input = None
	#sample output
	try:
		table_sample_output = table.find(text='Sample Output').findNext('div', {'class':'panel_content'})
		table_sample_output.hidden = True
	except Exception as e:
		table_sample_output = None

	# hint
	try:
		table_hint = table_sample_output.i.next.next
	except Exception as e:
		table_hint = None
	try:
		table_sample_output = table_sample_output.i.previous.previous.previous
	except Exception as e:
		pass
		
	# source
	try:
		table_source = table.find(text='Source').findNext('div', {'class':'panel_content'})
		table_source.hidden = True
	except Exception as e:
	   # print e
		table_source = None

	#recommend
	try:
		table_recommend = table.find(text='Recommend').findNext('div', {'class':'panel_content'})
		table_recommend.hidden = True
	except Exception as e:
	  #  print e
		table_recommend = None

	# author 
	try:
		table_author = table.find(text='Author').findNext('div', {'class':'panel_content'})
		table_author.hidden = True
	except Exception as e:
	  #  print e
		table_author = None

	info = []

	info.append(str(table_title))
	info.append(str(table_limit_des))
	info.append(str(table_problem_des))
	info.append(str(table_input))
	info.append(str(table_output))
	info.append(str(table_sample_input))
	info.append(str(table_sample_output))
	info.append(str(table_hint))
	info.append(str(table_author))
	info.append(str(table_source))
	info.append(str(table_recommend))
# len = 1
	return info


def store(start, end, url='http://acm.hdu.edu.cn/showproblem.php?pid='):
	engine = create_engine("mysql://root:duoduo@localhost:3306/test?charset=utf8", encoding="utf-8", echo=True)
	metadata = MetaData()
	hdoj_table = Table('hdoj', metadata,
			Column('problem_id', Integer, primary_key=True),
			Column('title', String(255), nullable=False),
			Column('limit_description', String(255), nullable=False),
			Column('problem_description', Text, nullable=False),
			Column('input', Text, nullable=False),
			Column('output', Text, nullable=False),
			Column('sample_input', Text, nullable=False),
			Column('sample_output', Text, nullable=False),
			Column('hint', Text, nullable=True),
			Column('author', String(40), nullable=True),
			Column('source', Text, nullable=True),
			Column('recommend', String(255), nullable=True),
			)

	class Hdoj(object):
		def __init__(self, problem_id, title, limit_description, problem_description, input, output, sample_input, sample_output, hint, author, source, recommend):						
			self.problem_id = problem_id
			self.title = title
			self.limit_description = limit_description
			self.problem_description = problem_description
			self.input = input
			self.output = output
			self.sample_input = sample_input 
			self.sample_output = sample_output
			self.hint = hint
			self.author = author
			self.source = source
			self.recommend = recommend
		
		def __repr__(self):
			return "<Hdoj('%s')>" % (self, title)
	
	metadata.create_all(engine)
	
	mapper(Hdoj, hdoj_table)
	
	Session = sessionmaker(autoflush=True, bind=engine)
	
	session = Session()
	
	data = []
	
	for i in range(start, end):
		problem_id = str(i)
		info = catch(url + problem_id)
		data.append(Hdoj(problem_id, info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9], info[10]))
	
	length = len(data)
	for i in range(length):
		try:
			session.add(data[i])
			session.flush()
			print 'adding'
		except Exception as e:
			#print 'exception'
			#print e
			session.rollback()
			pass
	
def start(begin, end):
	if(end < begin):
		print '输入有误，请检查您的输入。'
		return None

	default_group_num = 100
	groups = (end - begin) / default_group_num
	for i in range(groups):
		group_start = i * default_group_num + begin
		group_end = (i + 1) * default_group_num + begin
		store(group_start, group_end)
	if (end - begin) >= 0 :
		last_group_start = groups * default_group_num + begin
		store(last_group_start, end + 1)
