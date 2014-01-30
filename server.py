#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgitb
import cgi

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
#                print c.recv(1000)
                handle_connection(c)

def handle_connection(conn):


        mymessage = 'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            '<h1>Hello, world.</h1>' + \
            'This is rushjust\'s Web server.' +\
            '\r\n'
            

        conn_info = conn.recv(1000)

        page = ' '

        # split the info and save into requests arrray

        request = conn_info.split(' ')
        try:
                host = request[3].split('\r')
                host = host[0]

        except IndexError:
                host = '';
                
        # create the html content for the different pages
        conn.send(mymessage)

        # create 3 links for the 'main' page. Seperate links for content, files and images
         
        if request[1] == '/':
                index (request[1], host, conn)

        # create html for the content page
        elif request[1] == '/content':
                content(request[1], host, conn)

        # create html for the file page
        elif request[1] == '/file':
                file_page (request[1], host, conn)

        # create html for the image page
        elif request[1] == '/image':
                image (request[1], host, conn)

        # create message for post 
        elif request[0] == 'POST':
                form = cgi.FieldStorage()
                post_request (request[1], host, conn)

        #create message for submit page
        elif "submit?" in request[1]:
                get_request(request[1], host, conn)
        
        # if the text after the slash is not '', 'content', 'file', or 'image' then the page does not exist
        else:
                page = '<h2>This page does not exist!</h2>'

           
        conn.close()

def index (request, host, conn):
         contentLink = host + '/content'
         fileLink = host + '/file'
         imageLink = host + '/image'
         page = '<p><a href=\"http://' + contentLink + '\">Content</a>\r\n</p>' \
                '<p><a href=\"http://' + fileLink + '\">Files</a>\r\n</p>' \
                '<p><a href=\"http://' + imageLink + '\">Images</a></p>'+\
                '<form action= "/submit" method = "GET">' +\
                '<input type = "text" name ="firstname">' +\
                '<input type = "text" name = "lastname">' +\
                '<input type="submit" value="Submit">' +\
                '</form>'
         conn.send(page)

def content (request, host, conn):
        page = 'This is the content page.'
        conn.send(page)

def file_page (request, host, conn):
        page = 'This is the file page.'
        conn.send(page)

def image (request, host, conn):
        page = 'This is the image page.'
        conn.send(page)

def get_request (request, host, conn):
        request = request[8:]
        values = urlparse.parse_qs(request)
        if len(values) == 2:
                print values
                page = " <b> Hello Mr. {} {} </b>".format( values['firstname'][0], values['lastname'][0])
        else:
                page = "PLEASE ENTER A FIRST AND LAST NAME"
                
        conn.send(page)

def post_request (requests, host, conn):
#        form = web.input()
#        form = cgi.FieldStorage()
#        firstname = form['firstname'].value
#        print form
#       page = 'Hello Mr. {} {}'.format(form["firstname"], form["lastname"])
        page = ""
        conn.send(page)
        
if __name__ == '__main__':
        main()

