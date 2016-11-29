
import psycopg2
import psycopg2.extras

import sys

try:
    conn = psycopg2.connect("dbname='magoo' user='magoo'")
    
    cur = conn.cursor()

    
    query = "create table newsArticles (url varchar(220), title varchar(200), link varchar(220))"

    cur.execute(query) 
    
    conn.commit()
    
except psycopg2.DatabaseError as e:
    print ("insert failed??? Error %s" % e)
    sys.exit(1)
    
finally:
    if conn:
        conn.close()
    

