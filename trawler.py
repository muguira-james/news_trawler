
# -*- coding: utf-8 -*-
import time
import os, sys
import psycopg2
import psycopg2.extras

from multiprocessing import Process, Queue
import logging
import json

from rss_plugin import rss_worker
from rss_cnn_plugin import cnn_worker

# ====================================================
#
# refreash the rss_url_db from the db
#
def get_rss_feed_database(fileName):
    # the file is a simple name,link format
    rss_url_file = open('rss_url_db.json', 'r')
    for line in rss_url_file:
        # there are 3 items: name of the worker, source, and the url
        items = line.rstrip().split(',')
        rss_urls[items[1]] = { 'worker_name': items[0], 'url': items[2] }

    for i in rss_urls.iteritems():
        worker_name = i[1]['worker_name']
        url = i[1]['url']
        logging.info('{:20} {:12} {}'.format(i[0], worker_name, url))
#
# answer the last date/time the rss_url_db was
#  modified
#
def get_lastModified(fileName):
    return os.path.getmtime(fileName)
#
# deal with duplicate items
#
def handle_dups(js):
    """
    input is a json object. no output
    
    We undo the json,use the title to see if this article in in the news DB.
    - if it is just return
    - else save this article to the db (url or source, title, link to article)
    log this article
    """
    # qst is a string rep of the title to check for
    query = 'select * from newsarticles where title = %(title)s'
    try:
        url = js['source']
        title = js['title'].encode('UTF-8', 'replace')
        link = js['link']
        
        cursor.execute(query, {'title':title})    
        
        count = cursor.rowcount
        #print('{}: title={:30}'.format(count, js['title'].encode('UTF-8', 'replace')))
        if count != 0:
            return
        
        # this is a new item, insert it into the db and log it
        query = "insert into newsArticles (url, title, link) values (%s, %s, %s)"
    
        cursor.execute(query, (url, title, link)) 
        
        connection.commit()
        print (title)
        logging.info(title)
        
    except psycopg2.DatabaseError as e:
        print ("insert failed??? Error %s" % e)
        sys.exit(1)
# ====================================================
# ----------------------------------------------------------

logging.basicConfig(filename='log.log',
                    format='%(asctime)s %(message)s:',
                    level=logging.DEBUG)

logging.info('Trawler startup:')
logging.info('Step 0: fetch configuration structure')

config = json.loads(open('config.conf', 'r').read())
config['configFile_lastModified'] = get_lastModified('config.conf')

logging.info('configuration: ' + config['name_version'])

logging.info('Step 1: db connection')

try:
    connectionString = "dbname=\'" + config['postgres_dbname'] + "\' user=\'" + config['postgres_user_name'] + "\'"
    connection = psycopg2.connect(connectionString)
   
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
except psycopg2.DatabaseError as e:
    print ("opening the DB failed??? Error %s" % e)
    sys.exit(1)
    
logging.info('Step 2: fetch the rss url database')
#
# GLOBAL variables !!!!!
#
rss_urls = {}
out_q = Queue()   # multiprocessing queue
procs = []   # list of processes
#
config['rss_lastModified'] = get_lastModified(config['rss_url_db'])
get_rss_feed_database(config['rss_url_db'])
# -------------- Main loop ------------------------------------

logging.info('Getting to work now: running main loop')
time.sleep(1)

while True:
    # check to see if the rss db changed
    if get_lastModified(config['rss_url_db']) != config['rss_lastModified']:
        get_rss_feed_database(config['rss_url_db'])
        config['rss_lastModified'] = get_lastModified(config['rss_url_db'])
        
    # check to see if configuration has changed
    if get_lastModified('config.conf') != config['configFile_lastModified']:
        config = json.loads(open('config.conf', 'r').read())
        config['configFile_lastModified'] = get_lastModified(config['config.conf'])

    # process the rss db
    logging.info('creating rss processes')
    for item in rss_urls.iteritems():
        #print('worker = {:18} url={}'.format(item[1]['worker_name'], item[1]['url']))
        if item[1]['worker_name'] == 'cnn_worker':
            p = Process(target=cnn_worker, args=(item[1]['url'], out_q))
        # elif item[1]['worker_name'] == 'reuters_worker':
        #    p = Process(target=reuters_worker, args=(item[1]['url'], out_q))
        else:
            p = Process(target=rss_worker, args=(item[1]['url'], out_q))
        procs.append(p)
        p.start()

    # after starting all the workers goto sleep for a short while
    time.sleep(2)

    # process the queue for potential new stuff
    nitems = out_q.qsize()
    for p in range(nitems):
        js = out_q.get()
        handle_dups(js)

    for p in procs:   # wait for all processess to finish
        p.join()

    time.sleep(2)   # sleep a few more seconds and repeat
