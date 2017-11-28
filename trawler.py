
# -*- coding: utf-8 -*-
"""
sample config file

"name_version": "news trawler, v1",
"mongoDB_hostConnectString": "DB_PORT_27017_TCP_ADDR",
"mongoDB_port": 27017,
"rss_url_db": "rss_url_db.json",
"trawler_sleep_time": 10,
"loggingLevel": "info",
"logFile": "log.txt",
"rss_lastModified": 0

This is a long running process to gather news from various sources

For each source, gather the article title, the link to the actual story
the rss feed url.  Use gensim to get keywords, and summary

"""

import time
import os
from pymongo import MongoClient

from multiprocessing import Process, Queue
import logging
import json

import argparse
from rss_plugin import rss_worker
# from rss_cnn_plugin import cnn_worker

from reuters_plugin import reuters_worker
import requests

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

    for i in rss_urls.items():
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
    qst = {}
    # print 'handle_dups: looking for {}'.format(js['title'].encode('UTF-8', 'replace'))
    qst['title'] = js['title']
    # print '{} : {}'.format(db.news.find(qst), db.news.find(qst).count())
    count = db.news.find(qst).count()
    if count != 0:
        return
    # print 'injecting {}'.format(js['title'].encode('UTF-8', 'replace'))
    # this is a new item, insert it into the db and log it
    db.news.insert_one(js)
    # print js['title'].encode('UTF-8', 'replace')
    logging.info(js['title'].encode('UTF-8', 'replace'))

# ====================================================
# ------------------ main ----------------------------------

# parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--configuration", required=True,
	help="path to the config file")

args = vars(ap.parse_args())

# setup logging
logging.basicConfig(filename='log.log',
                    format='%(asctime)s %(message)s:',
                    level=logging.DEBUG)

logging.info('Trawler startup:')
logging.info('Step 0: fetch configuration structure')

# bring in the run-time configuration (from cmd line!!)
config = json.loads(open(args['configuration'], 'r').read())
print(config)
config['configFile_lastModified'] = get_lastModified('config.conf')

logging.info('configuration: ' + config['name_version'])

logging.info('Step 1: mongo db connection')
"""

This took run-time configuration from environment

logging.info('host = {}: {}'.format(os.environ[config['mongoDB_hostConnectString']],
                              str(config['mongoDB_port'])))

client = MongoClient(os.environ[config['mongoDB_hostConnectString']],
                                config['mongoDB_port'])
db = client.news
"""

# set up mongoDB
logging.info('host = {}: {}'.format(config['mongoDB_hostConnectString'],
                              str(config['mongoDB_port'])))

client = MongoClient(config['mongoDB_hostConnectString'],
                                config['mongoDB_port'])
db = client.news

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

#
# loop forever
while True:
    # check to see if the rss db changed
    if get_lastModified(config['rss_url_db']) != config['rss_lastModified']:
        get_rss_feed_database(config['rss_url_db'])
        config['rss_lastModified'] = get_lastModified(config['rss_url_db'])

    # check to see if configuration changed
    if get_lastModified('config.conf') != config['configFile_lastModified']:
        config = json.loads(open('config.conf', 'r').read())
        config['configFile_lastModified'] = get_lastModified(config['config.conf'])

    # process the rss db
    logging.info('creating rss processes')
    for item in rss_urls.items():
        #print('worker = {:18} url={}'.format(item[1]['worker_name'], item[1]['url']))
        if item[1]['worker_name'] == 'rss_reuters_worker':
            p = Process(target=reuters_worker, args=(item[1]['url'], out_q))
        else:
            p = Process(target=rss_worker, args=(item[1]['url'], out_q))
        procs.append(p)
        p.start()

    # after starting all the workers goto sleep for a short while
    time.sleep(2)

    # process the queue for potential new stuff
    #
    # loop reading new stuff from the queue
    while not out_q.empty():
        js = out_q.get()
        handle_dups(js)

    # wait for all processes to join
    for p in procs:   # wait for all processess to finish
        p.join()

    time.sleep(2)   # sleep a few more seconds and repeat
