# Basic LinkedIn API to retrieve your network information and export them into a csv file

from collections import defaultdict
import json

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd

# Part 1) register your API and get your LinkedIn API key at
# http://developer.linkedin.com/documents/authentication 
# Choose r_network for your registration

user_token = 'insert user token'
user_secret = 'insert user secret'

api_key = 'insert api key'
secret_key = 'insert secret key'


# Part 2) scraping your data using the LinkedIn API. 

import oauth2 as oauth
import urlparse
        
def request_token(consumer):
    client = oauth.Client(consumer)
    request_token_url = 'https://api.linkedin.com/uas/oauth/requestToken?scope=r_network'
    resp, content = client.request(request_token_url, "POST")
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
    request_token = dict(urlparse.parse_qsl(content))
    return request_token

def authorize(request_token):
    authorize_url ='https://api.linkedin.com/uas/oauth/authorize'
    print "Go to the following link in your browser:"
    print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
    print
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = raw_input('Have you authorized me? (y/n) ')
    oauth_verifier = raw_input('What is the PIN? ')
    return oauth_verifier

def access(consumer, request_token, oauth_verifier):
    access_token_url = 'https://api.linkedin.com/uas/oauth/accessToken'
    token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)
    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))
    return access_token

consumer = oauth.Consumer(api_key, secret_key)

r_token = request_token(consumer)
print "Request Token: oauth_token: %s, oauth_token_secret: %s" % (r_token['oauth_token'], r_token['oauth_token_secret'])
print

oauth_verifier = authorize(r_token)

a_token = access(consumer, r_token, oauth_verifier)
print a_token
print "Access Token: oauth_token = %s, oauth_token_secret = %s" % (a_token['oauth_token'], a_token['oauth_token_secret'])
print "You may now access protected resources using the access tokens above."
print


# Part 3) Download your network data, then clean and store it in csv file
import simplejson
import codecs
 
output_file = 'linkedIn_yourname_links.csv'
my_name = 'Insert your name'
 
def linkedin_connections():
    # Use your credentials to build the oauth client
    consumer = oauth.Consumer(key=api_key, secret=secret_key)
    token = oauth.Token(key=a_token['oauth_token'], secret=a_token['oauth_token_secret'])
    client = oauth.Client(consumer, token)
    
    # Fetch first degree connections
    resp, content = client.request('http://api.linkedin.com/v1/people/~/connections?format=json')
    results = simplejson.loads(content)
    
    # File that will store the results
    output = codecs.open(output_file, 'w', 'utf-8')
    
    # Loop through the 1st degree connection and see how they connect to each other
    for result in results["values"]:
        con = "%s %s" % (result["firstName"].replace(",", " "), result["lastName"].replace(",", " "))
        print >>output, "%s,%s" % (my_name, con)
        # This is the trick, use the search API to get related connections
        u = "https://api.linkedin.com/v1/people/%s:(relation-to-viewer:(related-connections))?format=json" % result["id"]
        resp, content = client.request(u)
        rels = simplejson.loads(content)
        try:
            for rel in rels['relationToViewer']['relatedConnections']['values']:
                sec = "%s %s" % (rel["firstName"].replace(",", " "), rel["lastName"].replace(",", " "))
                print >>output, "%s,%s" % (con, sec)
        except:
            pass

linkedin_connections()

from operator import itemgetter
from unidecode import unidecode
 
clean_output_file = 'linkedIn_clean.csv'
 
def stringify(chain):
    # Simple utility to build the nodes labels
    allowed = '0123456789abcdefghijklmnopqrstuvwxyz_'
    c = unidecode(chain.strip().lower().replace(' ', '_'))
    return ''.join([letter for letter in c if letter in allowed])
 
 
def clean(f_input, f_output):
    output = open(f_output, 'w')
    # Store the edges inside a set for dedup
    edges = set()
    for line in codecs.open(f_input, 'r', 'utf-8'):
        from_person, to_person = line.strip().split(',')
        _f = stringify(from_person)
        _t = stringify(to_person)
        # Reorder the edge tuple
        _e = tuple(sorted((_f, _t), key=itemgetter(0, 1)))
        edges.add(_e)
    for edge in edges:
        print >>output, '%s,%s' % (edge[0], edge[1])
 
clean(output_file, clean_output_file)
