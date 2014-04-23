# middleware playback
class MiddlewarePlayback:
    def __init__(self, application):
        self.application = application
    def __call__(self, environ, start_response):
        print "~~~~environ~~~~\n"
        for key in environ.keys():
	    print "%s : %s"%(key, environ[key])
	response_list = self.application(environ, start_response)
	print "\n~~~~response_list~~~~\n"
	for item in response_list:
	    print item
	print "\n"
	return response_list