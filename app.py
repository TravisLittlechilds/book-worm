from flask import Flask, url_for, render_template, request, redirect, flash
from rauth import OAuth1Service, OAuth1Session
from bs4 import BeautifulSoup
import lxml
import urlparse
from tokens import *

app = Flask(__name__, static_url_path='/static')

# https://www.goodreads.com/api/oauth_example
  
def make_session():
    
    goodreads_session = OAuth1Session(
    consumer_key = CONSUMER_KEY,
    consumer_secret = CONSUMER_SECRET,
    access_token = ACCESS_TOKEN,
    access_token_secret = ACCESS_TOKEN_SECRET,
    )
    return goodreads_session
  
# Flask Stuff

@app.route('/')
def main_page():    
    return render_template('index.html')
    

@app.route('/add', methods=['POST'])    
def add_book(): 

    # don't know why but this needs to be re-made each request or it fails (404)
    # was in main as a global, but that caused it to only work once
    
    goodreads_session = make_session()
    
    # book_id 631932 is "The Greedy Python"
    data = {'name': 'to-read', 'book_id': 631932}

    # add this to our "to-read" shelf
    response = goodreads_session.post('http://www.goodreads.com/shelf/add_to_shelf.xml', data)

    if response.status_code != 201:
        flash('There was an error, it was ' + str(response.status_code))
        print response.content
        return redirect(url_for('main_page'))
    else:
        flash("You've successfully added The Greedy Python")
        print 'Book added!'
    return redirect(url_for('main_page'))
    
@app.route('/get_list', methods=['GET'])
def get_list():

    goodreads_session = make_session()

    data = {
    'v': '2', 
    'id': '4200483',
    'shelf': 'to-read',
    'per_page': '46'
    }
#
    shelf_list = goodreads_session.get('http://www.goodreads.com/review/list.xml', params=data)

    goodreads_soup = BeautifulSoup(shelf_list.content, "lxml")
    
    title_list = goodreads_soup.findAll('title')
    for each_title in title_list:
        print each_title.string

    return render_template('index.html', title_list=title_list )
    

@app.route('/get_userid', methods=['POST','GET'])
def get_user_id():
# my userid = 4200483
    response = goodreads_session.get('http://www.goodreads.com/api/auth_user')
    if response.status_code != 200:
       raise Exception('Cannot fetch resource: %s' % response.status_code)
    else:
        print 'this works2', response.content
    return redirect(url_for('main_page'))


    
    
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)


