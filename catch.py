#! -*- encoding:utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup
def catch(url=None):
    content_stream = urllib2.urlopen(url)
    content = content_stream.read()
    soup = BeautifulSoup(content)
    table = soup.table
    #title
    table_title = table.find('h1')
    #title below limits description
    table_limit_des = table_title.findNext('span')
    # problem description, input, output, sample input, sample output
    table_content = table.findAll('div',{'class' : 'panel_content'},limit = 5)
    for i in table_content:
        i.hidden = True
    # hint
    table_hint = None
    try:
        table_hint = table_content[4].i.next.next
    except Exception as e:
     #   print e
        table_hint = None
    try:
        table_content[4] = table_content[4].i.previous.previous.previous
    except Exception as e:
     #   print e
        pass
        
    # source
    try:
        table_source = table.find(text='Source').findNext('div',{'class':'panel_content'})
        table_source.hidden = True
    except Exception as e:
       # print e
        table_source = None

    #recommend
    try:
        table_recommend = table.find(text='Recommend').findNext('div',{'class':'panel_content'})
        table_recommend.hidden = True
    except Exception as e:
      #  print e
        table_recommend = None

    # author 
    try:
        table_author = table.find(text='Author').findNext('div',{'class':'panel_content'})
        table_author.hidden = True
    except Exception as e:
      #  print e
        table_author = None

    info = []
    for i in table_content:
        info.append(str(i))

    info.append(str(table_hint))
    info.append(str(table_author))
    info.append(str(table_source))
    info.append(str(table_recommend))
    return info


##    table_font = table.findAll('font')
    #print table_title
#    for i in info:
        #print '==================================='
        #print i
    #return info
##    print table_font[-1]
##    print '----------------------------------------------------'
##    problem_title = table.findAll('div',{'class':'panel_title'})
##    problem_text = table.findAll('div',{'class':'panel_content'})
##    length = len(problem_title)
##    for i in range(length):
##        print problem_title[i]
##        print problem_text[i]
##        print '----------------------------------------------------'
##    #.prettify()
##
