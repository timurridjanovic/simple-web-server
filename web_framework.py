from paste.request import parse_formvars

def serve_page(page, template_vars=None):
    with open ("./views/" + page + ".html", "r") as p:
        template = p.readlines()
        if template_vars == None:
            return template
        for e in template_vars.keys():
            template = [line.replace("{{" + e + "}}", template_vars[e]) for line in template]
        return template

def serve_css(path):
    try:
        with open("./" + path, "r") as p:
            return p.readlines()
    except IOError:
            return ["no such file"]
            

def serve_javascript(path):
    try:
        with open("./" + path, "r") as p:
            return p.readlines()
    except IOError:
            return ["no such file"]

def app(environ, start_response):
    if environ['REQUEST_METHOD'] == 'GET':
        return handle_get_request(environ, start_response)

    elif environ['REQUEST_METHOD'] == 'POST':
        return handle_post_request(environ, start_response)
    else:
        start_response('200 OK', [('content-type', 'text/html')])
        return ["We just handle get and post requests"]

def handle_get_request(environ, start_response):
    static_files = [e for e in environ['PATH_INFO'].split("/") if e]
    
    if environ['PATH_INFO'] in router:
        path = environ['PATH_INFO']
        start_response('200 OK', [('content-type', 'text/html')])
        return router[path].get()
    
    elif static_files[0] == "css" and len(static_files) > 1:
        start_response('200 OK', [('content-type', 'text/css')])
        return serve_css(environ['PATH_INFO'])

    elif static_files[0] == "js" and len(static_files) > 1:
        start_response('200 OK', [('content-type', 'application/javascript')])
        return serve_javascript(environ['PATH_INFO'])

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
        return serve_page("index", {"name": "Timur", "phone": "444-999-7777"})

    @classmethod
    def post(self, fields):
        return serve_page("index", fields)
        

class Hello(object):
    @classmethod
    def get(self):
        return serve_page("hello")
    
    @classmethod
    def post(self, fields):
        return serve_page("hello", fields)
        

class Whut(object):
    @classmethod
    def get(self):
        return serve_page("whut")

    @classmethod
    def post(self, fields):
        return serve_page("whut", fields)
        



router = {
    "/": Index,
    "/hello": Hello,
    "/whut": Whut
}

if __name__ == '__main__':
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='5000')
