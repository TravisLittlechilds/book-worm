from flask import Flask, url_for, render_template, request, redirect, flash
from rauth import OAuth1Service, OAuth1Session
import urlparse, logging
import xml.etree.ElementTree as ET
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

    # don't know why but this needs to be re-made each request or it fails (404)
    # was in main as a global, but that caused it to only work once
    goodreads_session = OAuth1Session(
    consumer_key = CONSUMER_KEY,
    consumer_secret = CONSUMER_SECRET,
    access_token = ACCESS_TOKEN,
    access_token_secret = ACCESS_TOKEN_SECRET,
    )
    
    # book_id 631932 is "The Greedy Python"
    data = {'name': 'to-read', 'book_id': 631932}

    # add this to our "to-read" shelf
    response = goodreads_session.post('http://www.goodreads.com/shelf/add_to_shelf.xml', data)
    print '----worked----' + str(data)
    print response.content
    print '----worked---'

    if response.status_code != 201:
        flash('There was an error, it was ' + str(response.status_code))
        print response.content
        return redirect(url_for('main_page'))
    else:
        flash("You've successfully added The Greedy Python")
        print 'Book added!'
    return redirect(url_for('main_page'))
    
@app.route('/get_list', methods=['POST'])
def get_list():
    pass
    return
    
#@app.route('/get_userid', methods=['POST','GET'])
#def getUserId():
# my userid = 4200483
#    response = goodreads_session.get('http://www.goodreads.com/api/auth_user')
#    if response.status_code != 200:
#       raise Exception('Cannot fetch resource: %s' % response.status_code)
#    else:
#        print 'this works2', response.content
#    return render_template(url_for('main_page'))


    
    
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)


