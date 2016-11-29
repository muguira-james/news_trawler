import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
print '{} {}'.format(os.environ['DB_PORT_27017_TCP_ADDR'], '27017')
db = client.news


@app.route('/')
def todo():

    count = db.news.find().count()
    print("total news articles = %d", count)
    _items = db.news.find()
    items = [item for item in _items]

    return render_template('todo.html', items=items, tot=count)


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
