#!/usr/bin/env python
import random
import socket
import time

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
		print 'Got connection from', client_host, client_port
		handleconnection(c)
		
def handle_connection(conn):
	# send a response
	conn_info = conn.recv(1000)
	page = ' '
	request = conn_info.split(' ')
	try:
		host = request[3].split('\r')
		host = host[0]

	except IndexError:
		host = '';

                
	# create the html content for the different pages
	# create 3 links for the 'main' page. Seperate links for content, files and images
        
	if request[1] == '/':
		page = 'HTTP/1.0 200 OK\r\n' + \
		    'Content-type: text/html\r\n' + \
			'\r\n' + \
			'<h1>Links to other pages</h1>' + \
			'<a href = /content>Content</a><br>' + \
			'<a href = /file>File</a><br>' + \
			'<a href = /image>Image</a>'

        # create html for the content page
	elif request[1] == '/content':
	   page = 'This is the content page.'

        # create html for the file page
	elif request[1] == '/file':
	   page = 'This is the file page.'

        # create html for the image page
	elif request[1] == '/image':
	   page = 'This is the image page.'

        # create message for 
	elif request[0] == 'POST':
		page = 'Heyyyyy'
                
        # if the text after the slash is not '', 'content', 'file', or 'image' then the page does not exist
	else:
	   page = '<h2>This page does not exist!</h2>'

			
			
	conn.send('HTTP/1.0 200 OK\r\n')
	conn.send('Content-type: text/html\r\n')
	conn.send('\r\n')
	conn.send('<h1>Hello, world.</h1>')
	conn.send('This is DuncanCYoung\'s Web server.')
	
	conn.send(page)
	conn.close()
    
   

if __name__ == '__main__':
    main()
