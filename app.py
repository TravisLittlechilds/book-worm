from flask import Flask, url_for, render_template
from rauth import OAuth1Service, OAuth1Session
import urlparse
from tokens import *

app = Flask(__name__)

# https://www.goodreads.com/api/oauth_example

print CONSUMER_KEY    

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

if response.status_code != 201:
    raise StandardError('Cannot create resource: %s' % response.status_code)
else:
    print 'Book added!'

# Flask Stuff
#
#@app.route('/')
#def hello_world():
#    return render_template('index.html')
#    
#if __name__ == '__main__':
#    app.run(debug=True)
