
import psycopg2
import psycopg2.extras

import sys


zz = {}

zz['url'] = '	http://rss.cnn.com/rss/cnn_topstories.rss'
zz['title'] = 'Wildfires threaten aquarium with 1500 animals in Gatlinburg,TN'
zz['link'] = 'http://www.cnn.com/2016/11/28/us/southern-fires-gatlinburg-smokies/index.html?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+rss%2Fcnn_topstories+%28RSS%3A+CNN+-+Top+Stories%29'


try:
    conn = psycopg2.connect("dbname='magoo' user='magoo'")
    
    cur = conn.cursor()
    tit = 'Wildfires threaten aquarium with 1500 animals in Gatlinburg,TN'
   
    query2 = 'select * from newsarticles where title = %(title)s'
    cur.execute(query2, {'title':tit})
    count = cur.rowcount
    if count != 0:
        print("found an article where I should not have")
        sys.exit(0)
        
    query = "insert into newsArticles (url, title, link) values (%s, %s, %s)"

    cur.execute(query, (zz['url'],zz['title'],zz['link'])) 
    
    conn.commit()
    
except psycopg2.DatabaseError as e:
    print ("insert failed??? Error %s" % e)
    sys.exit(1)
    
finally:
    if conn:
        conn.close()
    
