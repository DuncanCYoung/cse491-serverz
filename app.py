# from http://docs.python.org/2/library/wsgiref.html

import cgi
import urlparse
import jinja2
import os
import traceback
import urllib
from StringIO import StringIO
from wsgiref.util import setup_testing_defaults

def app(environ, start_response):
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)

    # By default, set up the 404 page response. If it's
    # a valid page, we change this. If some weird stuff
    # happens, it'll default to 404.
    status = '404 Not Found'
    response_content = not_found('', env)
    headers = [('Content-type', 'text/html')]
    
    try:
        http_method = environ['REQUEST_METHOD']
        path = environ['PATH_INFO']
    except:
        pass

    if http_method == 'POST':
        if path == '/':
            # I feel like there's a better way of doing this
            # than spamming status = '200 OK'. But it's almost 10
            # and we have to catch up because our capstone group
            # member just didn't do anything the past week. /rant
            status = '200 OK'
            response_content = handle_index(environ, env)
        elif path == '/submit':
            status = '200 OK'
            response_content = handle_submit_post(environ, env)
    elif http_method == 'GET':
        print path
        if path == '/':
            status = '200 OK'
            response_content = handle_index(environ, env)
        elif path == '/content':
            status = '200 OK'
            response_content = handle_content(environ, env)
        elif path == '/file':
            headers = [('Content-type', 'text/plain')]
            status = '200 OK'
            response_content = handle_file(environ, env)
        elif path == '/image':
            headers = [('Content-type', 'image/jpeg')]
            status = '200 OK'
            response_content = handle_image(environ, env)
        elif path == '/submit':
            status = '200 OK'
            response_content = handle_submit_get(environ, env)
        elif path == '/thumbnails':
            headers = [('Content-type', 'text/html')]
            status = '200 OK'
            response_content = handle_thumbnails(environ, env)
        elif path[0:5] == '/pics':
            headers = [('Content-type', 'image/png')]
            status = '200 OK'
            response_content = pics(environ, env)
                
    start_response(status, headers)
    response = []
    response.append(response_content)
    return response

def make_app():
    return app

def handle_index(params, env):
    return str(env.get_template("index_result.html").render())
    
def handle_content(params, env):
    return str(env.get_template("content_result.html").render())

def readFile(filepath):
    ''' Reads a file and returns its contents as a string '''
    f = open(filepath, 'rb')
    data = f.read()
    f.close()

    return data

def handle_file(params, env):
    return readFile('./files/nope.txt')

def handle_image(params, env):
    return readFile('./images/beermug.png')
    

def not_found(params, env):
    return str(env.get_template("not_found.html").render())

def handle_submit_post(environ, env):
    ''' Handle a connection given path /submit '''
    # submit needs to know about the query field, so more
    # work needs to be done here.

    # we want the first element of the returned list
    headers = {}
    for k in environ.keys():
        headers[k.lower()] = environ[k]

    form = cgi.FieldStorage(headers = headers, fp = environ['wsgi.input'], 
                            environ = environ)

    try:
      firstname = form['firstname'].value
    except KeyError:
      firstname = ''
    try:
      lastname = form['lastname'].value
    except KeyError:
      lastname = ''

    vars = dict(firstname = firstname, lastname = lastname)
    return str(env.get_template("submit_result.html").render(vars))

def handle_submit_get(environ, env):
    ''' Handle a connection given path /submit '''
    # submit needs to know about the query field, so more
    # work needs to be done here.

    # we want the first element of the returned list
    params = environ['QUERY_STRING']
    params = urlparse.parse_qs(params)

    try:
      firstname = params['firstname'][0]
    except KeyError:
      firstname = ''
    try:
      lastname = params['lastname'][0]
    except KeyError:
      lastname = ''

    vars = dict(firstname = firstname, lastname = lastname)
    return str(env.get_template("submit_result.html").render(vars))
    
def pics(environ, env):
    pic_file = './images' + environ['PATH_INFO'][5:]
    print pic_file
    return readFile(pic_file)
    
            
def handle_thumbnails(environ, env):
    list = []
    for file in sorted(os.listdir('images')):
        print file
        list.append(file)
    params = dict(names=list)
    print params;
    print str(env.get_template("thumbnails.html").render(params).encode('latin-1', 'replace'))
    return str(env.get_template("thumbnails.html").render(params).encode('latin-1', 'replace'))
