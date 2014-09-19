from paste.request import parse_formvars


def servePage(page, template_vars=None):
    with open (page + ".html", "r") as p:
        template = p.readlines()
        if template_vars == None:
            return template
        for e in template_vars.keys():
            template = [line.replace("{{" + e + "}}", template_vars[e]) for line in template]
        return template

def app(environ, start_response):
    if environ['REQUEST_METHOD'] == 'GET':
        return handle_get_request(environ, start_response)

    elif environ['REQUEST_METHOD'] == 'POST':
        return handle_post_request(environ, start_response)
    else:
        start_response('200 OK', [('content-type', 'text/html')])
        return ["Nope"]

def handle_get_request(environ, start_response):
    if environ['PATH_INFO'] in router:
        path = environ['PATH_INFO']
        start_response('200 OK', [('content-type', 'text/html')])
        return router[path].get()
    else:
        start_response('404 error', [('content-type', 'text/html')])
        return ["ERROR 404 sucka"]

def handle_post_request(environ, start_response):
    if environ['PATH_INFO'] in router:
        path = environ['PATH_INFO']
        fields = parse_formvars(environ)
        start_response('200 OK', [('content-type', 'text/html')])
        return router[path].post(fields)
    else:
        start_response('200 OK', [('content-type', 'text/html')])
        return ["ERROR 404"]

class Index(object):
    @classmethod
    def get(self):
        return servePage("index", {"name": "Timur", "phone": "444-999-7777"})

    @classmethod
    def post(self, fields):
        return servePage("index", fields)
        

class Hello(object):
    @classmethod
    def get(self):
        return servePage("hello")
    
    @classmethod
    def post(self, fields):
        return servePage("hello", fields)
        

class Whut(object):
    @classmethod
    def get(self):
        return servePage("whut")

    @classmethod
    def post(self, fields):
        return servePage("whut", fields)
        



router = {
    "/": Index,
    "/hello": Hello,
    "/whut": Whut
}

if __name__ == '__main__':
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='5000')
