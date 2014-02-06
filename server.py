#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse
from urlparse import parse_qs
import cgi
from StringIO import StringIO

def main():

        s = socket.socket()         # Create a socket object
        host = socket.getfqdn() # Get local machine name
        port = random.randint(8000, 9999)
        s.bind((host, port))        # Bind to the port

        print 'Starting server on', host, port
        print 'The Web server URL for this would be http://%s:%d/' % (host, port)

        s.listen(5)                 # Now wait for client connection.

        print 'Entering infinite loop; hit CTRL-C to exit'
        while True:
                # Establish connection with client.
                c, (client_host, client_port) = s.accept()
#               print c.recv(1000)
                handle_connection(c)

def handle_connection(conn):

        message = 'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            '<h1>Hello, world.</h1>' + \
            'This is youngdun\'s Web server.' +\
            '\r\n'

	request = conn.recv(1)

	# This will get all the headers
	while request[-4:] != '\r\n\r\n':
		request += conn.recv(1)

	first_line_of_request_split = request.split('\r\n')[0].split(' ')
	second_line  = request.split('\r\n')[1].split(' ')
	try:
		second_line = request.split('\r\n')[1].split(' ')
		host = second_line[1]
	except:
		host = ''


	# Path is the second element in the first line of the request
	# separated by whitespace. (Between GET and HTTP/1.1). GET/POST is first.
	http_method = first_line_of_request_split[0]

	try:
		parsed_url = urlparse(first_line_of_request_split[1])
		path = parsed_url[2]
	except:
	        path = "/404"

	# create the html content for the different pages
	conn.send(message)

	if http_method == 'POST':
		headers_dict, content = parse_post_request(conn, request)
		environ = {}
		environ['REQUEST_METHOD'] = 'POST'

		print request + content
		form = cgi.FieldStorage(headers = headers_dict, fp = StringIO(content), environ = environ)

		if path == '/':
			handle_index(path, conn)
		elif path == '/submit':
			# POST has the submitted params at the end of the content body
			post_request(form, host, conn)
		else:
			notfound(path, conn)



	# create links for the 'main' page. Seperate links for content, files and images
	else:
               
		if path == '/':
			index (path, host, conn)

		# create html for the content page
		elif path == '/content':
			content_page(path, host, conn)

		# create html for the file page
		elif path == '/file':
			file_page (path, host, conn)

		# create html for the image page
		elif path == '/image':
			image (path, host, conn)

		#create message for submit page
		elif path == '/submit':
			get_request(parsed_url[4], host, conn)

		# if the text after the slash is not '', 'content', 'file', or 'image' then the page does not exist
		else:
			not_found(path, host, conn)

   	
	conn.close()

def index (request, host, conn):
	 contentLink = host + '/content'
	 fileLink = host + '/file'
	 imageLink = host + '/image'
	 page = '<p><a href=\"http://' + contentLink + '\">Content</a>\r\n</p>' \
	        '<p><a href=\"http://' + fileLink + '\">Files</a>\r\n</p>' \
		'<p><a href=\"http://' + imageLink + '\">Images</a></p>'+\
		'<p><b>Form with POST</b></p>' +\
		'<form action= "/submit" method = "POST">' +\
		'<input type = "text" name ="firstname">' +\
		'<input type = "text" name = "lastname">' +\
		'<input type="submit" value="Submit">' +\
		'</form>' +\
		'<p><b>Form Submission via POST (multipart/form-data)</b></p>'+\
	        '<form action="/submit" method="POST" enctype="multipart/form-data">' + \
		'<input type="text" name="firstname">' + \
		'<input type="text" name="lastname">' + \
		'<input type="submit" value="Submit">' + \
		'</form>' + \
	        '<p><b>Form with GET</b></p>' +\
		'<form action= "/submit" method = "GET">' +\
		'<input type = "text" name ="firstname">' +\
		'<input type = "text" name = "lastname">' +\
		'<input type="submit" value="Submit">' +\
		'</form>'


	 conn.send(page)


def content_page (request, host, conn):
	page = 'This is the content page.'
	conn.send(page)

def file_page (request, host, conn):
	page = 'This is the file page.'
	conn.send(page)

def image (request, host, conn):
	page = 'This is the image page.'
	conn.send(page)

def get_request (request, host, conn):
	request = parse_qs(request)

	try:
		firstname = request['firstname'][0]
	except KeyError:
		firstname = ''

	try:
		lastname = request['lastname'][0]
	except KeyError:
		lastname = ''


	page = " <b> Hello Mr. %s %s</b>" % (firstname, lastname)
	conn.send(page)

def post_request (request, host, conn):
	try:
		firstname = request['firstname'].value
	except KeyError:
		firstname = ''

	try:
		lastname = request['lastname'].value
	except KeyError:
		lastname = ''

	page = "Hello Mr. %s %s" % (firstname, lastname)
	conn.send(page)

def not_found (request, host, conn):
	page = '<h2>PAGE NOT FOUND.</h2>'
	conn.send(page)


def parse_post_request(conn, request):
	# Takes in a request (as a string), parses it, and
	# returns a dictionary of header name => header value
	# returns a string built from the content of the request
	header_dict = dict()

	request_split = request.split('\r\n')

	# Headers are separated from the content by '\r\n'
	# which, after the split, is just ''.

	# First line isn't a header, but everything else
	# up to the empty line is. The names are separated
	# from the values by ': '

	for i in range(1,len(request_split) - 2):
		header = request_split[i].split(': ', 1)
		header_dict[header[0].lower()] = header[1]


	content_length = int(header_dict['content-length'])

	content = ''
	for i in range(0,content_length):
		content += conn.recv(1)

	return header_dict, content


if __name__ == '__main__':
        main()
