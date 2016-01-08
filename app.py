from flask import Flask, url_for, render_template, request, redirect, flash
from rauth import OAuth1Service, OAuth1Session
import urlparse, logging
from logging.handlers import RotatingFileHandler
from tokens import *

app = Flask(__name__, static_url_path='/static')

# https://www.goodreads.com/api/oauth_example
  
# Flask Stuff

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/add', methods=['POST'])    
def addBook(): 
    
    goodreads_session = OAuth1Session(
    consumer_key = CONSUMER_KEY,
    consumer_secret = CONSUMER_SECRET,
    access_token = ACCESS_TOKEN,
    access_token_secret = ACCESS_TOKEN_SECRET,
    )
    
    print 'Adding Greedy Python'
    # book_id 631932 is "The Greedy Python"
    data = {'name': 'to-read', 'book_id': 631932}

    # add this to our "to-read" shelf
    response = goodreads_session.post('http://www.goodreads.com/shelf/add_to_shelf.xml', data)

    if response.status_code != 201:
        flash('There was an error')
        raise StandardError('Cannot create resource: %s' % response.status_code)
    else:
        flash("You've successfully added The Greedy Python")
        print 'Book added!'
    return redirect(url_for('main_page'))
    
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)


