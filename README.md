# news_trawler (PYTHON 2.7 only!)
long running server to gather news from interesting sources

Demo of how to use docker-compose in a non-trivial setting.

## Contents:

+ trawler.py is the driver. This opens the logs, reads the configs, read the rss feed data base (rss_url_db.json) and loops pulling data from the various sources.

+ rss_plugin.py handles rss feed parsing

+ rss_cnn_plugin.py handle the specifics of cnn feeds

+ rss_url_db.json is a list of rss sites to parse

+ config.conf holds the app configuration info

## Docker stuff:

+ Dockerfile is the build file for the trawler app

+ docker-compose.yml is the compose build file

### Web

The admin interface for trawler.

+ app.py is a flask based app to handle html and interaction
+ Dockerfile the build file
+ requirements.txt pulls in required software
+ templates holds the html

install 

virtualenv news_trawler

cd news_trawler

source bin/activate

pip install -r requirements.txt --find-links file:///$PWD/pips


