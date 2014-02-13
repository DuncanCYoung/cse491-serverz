import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")

    # Set the different messages depending on the page
    
    expected_return = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n' + \
    '<h1>Hello, world.</h1>This is youngdun\'s Web server.\r\n' + \
    '<p><a href="http:///content">Content</a>\r\n</p>' + \
    '<p><a href="http:///file">Files</a>\r\n</p>' + \
    '<p><a href="http:///image">Images</a></p>' + \
    '<p><b>Form with POST</b></p>' + \
    '<form action= "/submit" method = "POST">' + \
    '<input type = "text" name ="firstname">' + \
    '<input type = "text" name = "lastname">' + \
    '<input type="submit" value="Submit"></form>' + \
    '<p><b>Form Submission via POST (multipart/form-data)</b></p>' + \
    '<form action="/submit" method="POST" enctype="multipart/form-data">' + \
    '<input type="text" name="firstname"><input type="text" name="lastname">' + \
    '<input type="submit" value="Submit"></form>' + \
    '<p><b>Form with GET</b></p><form action= "/submit" method = "GET">' + \
    '<input type = "text" name ="firstname">' + \
    '<input type = "text" name = "lastname">' + \
    '<input type="submit" value="Submit"></form>'
    
                      
    # Call the function in server.py with the different connections/pages set up at the top of this function
    server.handle_connection(conn)

    # Test to see if the hmtl matches
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_content():
    conn_content = FakeConnection("GET /content HTTP/1.0\r\n\r\n")

    # Set the different messages depending on the page
    content_return ='HTTP/1.0 200 OK\r\n' + \
                     'Content-type: text/html\r\n' + \
                     '\r\n' + \
                     '<h1>Hello, world.</h1>' + \
                     'This is youngdun\'s Web server.' + \
                     '\r\n' +\
                     'This is the content page.'                                                                               



    # Call the function in server.py with the different connections/pages set up at the top of this function
    server.handle_connection(conn_content)


    # Test to see if the hmtl matches
    assert conn_content.sent == content_return, 'Got: %s' % (repr(conn_content.sent),)

    
def test_file():
    conn_file = FakeConnection("GET /file HTTP/1.0\r\n\r\n")

    # Set the different messages depending on the page
    file_return = 'HTTP/1.0 200 OK\r\n' + \
                  'Content-type: text/html\r\n' + \
                  '\r\n' + \
                  '<h1>Hello, world.</h1>' + \
                  'This is youngdun\'s Web server.' + \
                  '\r\n' +\
                  'This is the file page.'


    # Call the function in server.py with the different connections/pages set up at the top of this function
    server.handle_connection(conn_file)

    # Test to see if the hmtl matches
    assert conn_file.sent == file_return, 'Got: %s' % (repr(conn_file.sent),)
    
    
def test_image():
    conn_image = FakeConnection("GET /image HTTP/1.0\r\n\r\n")


    # Set the different messages depending on the page
    image_return = 'HTTP/1.0 200 OK\r\n' + \
                   'Content-type: text/html\r\n' + \
                   '\r\n' + \
                   '<h1>Hello, world.</h1>' + \
                   'This is youngdun\'s Web server.' + \
                   '\r\n' + \
                   'This is the image page.'


    # Call the function in server.py with the different connections/pages set up at the top of this function
    server.handle_connection(conn_image)

    # Test to see if the hmtl matches
    assert conn_image.sent == image_return, 'Got: %s' % (repr(conn_image.sent),)   


def test_post():
    conn_post= FakeConnection("POST /submit HTTP/1.1\r\n\r\nfirstname=Duncan&lastname=Young")
    post_return =  'HTTP/1.0 200 OK\r\n' + \
                   'Content-type: text/html\r\n' + \
                   '\r\n' + \
                   '<h1>Hello, world.</h1>' + \
                   'This is youngdun\'s Web server.' + \
                   '\r\n' +\
                   'Hello Mr. Duncan Young.'
    
    server.handle_connection(conn_post)
    assert conn_post.sent == post_return, 'Got: %s' % (repr(conn_post.sent),)


def test_get():
        conn_get = FakeConnection("GET /submit?firstname=Justin&lastname=Rush HTTP/1.0\r\n\r\n")

        # Set the different messages depending on the page
        get_return = 'HTTP/1.0 200 OK\r\n' + \
                     'Content-type: text/html\r\n' + \
                     '\r\n' + \
                     '<h1>Hello, world.</h1>' + \
                     'This is youngdun\'s Web server.' +\
                     '\r\n ' +\
                     '<b> Hello Mr. Justin Rush</b>'

        # Call the function in server.py with the different connections/pages set up at the top of this function
        server.handle_connection(conn_get)

        # Test to see if the hmtl matches
        assert conn_get.sent == get_return, 'Got: %s' % (repr(conn_get.sent),)
                
def test_not_found():
        conn_not_found = FakeConnection("GET /DoesNotExist HTTP/1.0\r\n\r\n")
        
        # Set the different messages depending on the page
        not_found_return = 'HTTP/1.0 200 OK\r\n' + \
        'Content-type: text/html\r\n' + \
        '\r\n' + \
        '<h1>Hello, world.</h1>' + \
        'This is youngdun\'s Web server.' + \
        '\r\n' + \
        '<h2>PAGE NOT FOUND.</h2>'

        # Call the function in server.py with the different connections/pages set up at the top of this function
        server.handle_connection(conn_not_found)

        # Test to see if the hmtl matches
        assert conn_not_found.sent == not_found_return, 'Got: %s' % (repr(conn_not_found.sent),)

def test_handle_connection_post():
        conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")
        expected_return = 'HTTP/1.0 200 OK\r\n'+\
                          'Content-type: text/html\r\n\r\n'+\
                          '<h1>Hello, world.</h1>' +\
                          'This is youngdun\'s Web server.\r\n'+\
                          '<p><a href="http:///content">Content</a>\r\n</p>' +\
                          '<p><a href="http:///file">Files</a>\r\n</p>'+\
                          '<p><a href="http:///image">Images</a></p>'+\
                          '<p><b>Form with POST</b></p>'+\
                          '<form action= "/submit" method = "POST">'+\
                          '<input type = "text" name ="firstname">'+\
                          '<input type = "text" name = "lastname">'+\
                          '<input type="submit" value="Submit">'+\
						'<p><b>Form Submission via POST (multipart/form-data)</b></p>'+\
							'<form action="/submit" method="POST" enctype="multipart/form-data">' + \
						'<input type="text" name="firstname">' + \
						'<input type="text" name="lastname">' + \
						'<input type="submit" value="Submit">' + \
						'</form>' + \
                          '</form><p><b>Form with GET</b></p>'+\
                          '<form action= "/submit" method = "GET">'+\
                          '<input type = "text" name ="firstname">'+\
                          '<input type = "text" name = "lastname">'+\
                          '<input type="submit" value="Submit">'+\
                          '</form>'


        server.handle_connection(conn)
        assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
