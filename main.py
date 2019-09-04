import os
import json
import requests
import tornado.web
import tornado.ioloop

base_url = 'https://192.86.33.94:19443/cusregapi/AccountNo?acctno=100000001001'
headers = {'Content-Type': 'application/json'}
params = {
    'jql': 'project = EXM AND resolution is not EMPTY',
    'expand': 'changelog',
}

req = requests.get(base_url, headers=headers, params=params, auth=('ibmuser', 'ibmuser'), verify=False)

# print(req.content)

# app = Flask(__name__, static_url_path='')

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(req.content)

class resourceRequestHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.write("Querying tweet with id " + req.content)

class queryStringRequestHandler(tornado.web.RequestHandler):
    def get(self):
        n = int(self.get_argument("n"))
        r = "odd" if n % 2 else "even"

        self.write("the number " + str(n) + " is " + r)

class staticRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", basicRequestHandler),
        (r"/blog", staticRequestHandler),
        (r"/isEven", queryStringRequestHandler),
        (r"/tweet/([0-9]+)", resourceRequestHandler)
    ])

    app.listen(port)
    print("I'm listening on port specified")
    tornado.ioloop.IOLoop.current().start()
