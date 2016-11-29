# news_trawler (PYTHON 2.7 only!)
long running server to gather news from interesting sources

Demo of how to use docker-compose in a non-trivial setting.

## Contents:

+ trawler.py is the driver. This opens the logs, reads the configs, read the rss feed data base (rss_url_db.json) and loops pulling data from the various sources.

+ rss_plugin.py handles rss feed parsing

+ rss_cnn_plugin.py handle the specifics of cnn feeds

+ rss_url_db.json is a list of rss sites to parse

+ config.conf holds the app configuration info

## DB Stuff:

+ createNewsTable.py creates a new postgres table with the right schema

+ insertNews.py tests inserting and some other little "study" stuff

+ queryNews.py tests query for the number in the DB and a follow on grab of everything

## Docker stuff (does not work on branch hana0):

+ Dockerfile is the build file for the trawler app

+ docker-compose.yml is the compose build file

The branch hana0 does not use docker.  Simply start trawler (python trawler.py) and 
start web/app.py from different terminals.  This assumes the postgres DB is up and 
running as a service in the background.

### Web

The admin interface for trawler.

+ app.py is a flask based app to handle html and interaction
+ Dockerfile the build file
+ requirements.txt pulls in required software
+ templates holds the html
