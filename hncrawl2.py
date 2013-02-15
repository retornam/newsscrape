#!/usr/bin/env python
import urllib2
import sqlite3
import datetime
from BeautifulSoup import BeautifulSoup as Soup
from soupselect import select

DATABASE="./hn.db"
connection = sqlite3.connect(DATABASE)

request = urllib2.Request('http://news.ycombinator.com')
request.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:15.0) Gecko/20120101 Firefox/15.0.1')
opener = urllib2.build_opener()

soup = Soup(opener.open(request).read())
links = select(soup, '.title a')
with connection:
    thedate = datetime.datetime.now()
    todaysdate = "%s" % thedate.strftime("%d-%h-%Y")
    getyesterdaysdate = datetime.date.today() - datetime.timedelta(1)
    yesterdaysdate = getyesterdaysdate.strftime("%d-%h-%Y")
    print "Todays date is %s" % todaysdate
    print "Yesterday was %s" % yesterdaysdate
    dateargs = "'" + todaysdate + "%'" + " or date_added like '" + yesterdaysdate + " %'"
    print dateargs
    query = "select * from links where date_added like %s " % dateargs
    cursor = connection.cursor()
    cursor.execute(query)
    #sqlite returns a unicode tuple so I need to convert
    #query results back to string
    rows = [str(a[1]) for a in cursor.fetchall()]
    for link  in links:
        if link['href'] == 'news2':
            pass
        elif link['href'] in rows:
            print 'I\'m already here'
            pass
        else:
            print link.string
            print link['href']
            d= datetime.datetime.now()
            cursor.execute("INSERT INTO links(link, title, date_added) VALUES (?, ? ,?)", (link['href'], link.string, d.strftime("%d-%h-%Y  %H:%M:%S"),) )
            connection.commit()
connection.close()
