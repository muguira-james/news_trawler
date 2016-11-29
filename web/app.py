# -*- coding: utf-8 -*-
import sys
from flask import Flask, redirect, url_for, request, render_template
import psycopg2
import psycopg2.extras
import json


app = Flask(__name__)


connectionString = ''
connection = ''
cursor = ''

@app.route('/')
def todo():


    query = 'select * from newsarticles'
        
    cursor.execute(query)    
    
    count = cursor.rowcount
    print('found {} articles in newsarticles'.format(count))
        
    query = "select * from newsarticles"
    
    cursor.execute(query) 
 
    ii = []
    rows = cursor.fetchall() # returns a list
    for row in rows:
        zz = {}
        tt = unicode(row[1], 'UTF-8')
        zz['title'] = tt
        zz['source'] = row[0]
        ii.append(zz)
    #items.append('{ u\"title\": u\"' + tt + '\", u\"source\": u\"' + row[0] + '\"}')
    aa = json.dumps(ii)
    print(aa)
    
    return render_template('todo.html', items=ii, tot=count)

"""
@app.route('/deleteOne', methods=['POST'])
def deleteOne():

    item_doc = {
        'title': request.form['title'],
        'source': request.form['source']
    }
    db.news.delete_one(item_doc)

    return redirect(url_for('todo'))

@app.route('/clear')
def clear():
    db.news.delete_many({})
    return redirect(url_for('todo'))

"""
if __name__ == "__main__":
    config = json.loads(open('config.conf', 'r').read())
    try:
        connectionString = "dbname=\'" + config['postgres_dbname'] + "\' user=\'" + config['postgres_user_name'] + "\'"
        connection = psycopg2.connect(connectionString)
       
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
    except psycopg2.DatabaseError as e:
        print ("opening the DB failed??? Error %s" % e)
        sys.exit(1)
    app.run(host='0.0.0.0', debug=True)
