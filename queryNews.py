# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 15:07:28 2016

@author: magoo
"""

import psycopg2
import psycopg2.extras
import sys


try:
    conn = psycopg2.connect("dbname='magoo' user='magoo'")
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    """
    query = "select * from newsarticles"
    
    cur.execute(query) 
    
    rows = cur.fetchall() # returns a list
    for row in rows:
        print ("{:10}| {:15}| {:30}".format(row[0][:10], row[1][:15], row[2][:30]))
    """
    # fictional title
    tit = 'Wildfires threaten aquarium with 1500 animals in Gatlinburg,TN'
   
    query2 = 'select * from newsarticles where title = %(title)s'
    cur.execute(query2, {'title':tit})
    rows = cur.fetchall()
    for row in rows:
        print ("{:10}| {:15}| {:30}".format(row['url'][:10], row['title'][:15], row['link'][:30]))

except psycopg2.DatabaseError as e:
    print ("insert failed??? Error %s" % e)
    sys.exit(1)
    
finally:
    if conn:
        conn.close()
    
