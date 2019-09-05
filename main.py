import os
import json
import requests
import tornado.web
import tornado.ioloop
import tornado.autoreload

base_url = 'https://192.86.33.94:19443/cusregapi/AccountNo?acctno=100000001001'
headers = {'Content-Type': 'application/json'}



# print(req.content)

# app = Flask(__name__, static_url_path='')

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        #req = requests.get(base_url, headers=headers, auth=('ibmuser', 'ibmuser'), verify=False)
        # self.write("main_modified")
        self.render("static/register.html")

class postedForm(tornado.web.RequestHandler):
    def post(self):
        base_url = 'https://192.86.33.94:19443/cusregapi/AccountNo?acctno='
        # 100000001001 is the only working answer
        end_url= base_url+str(self.get_body_argument("accnt"))
        req = requests.get(end_url, headers=headers, auth=('ibmuser', 'ibmuser'), verify=False)
        json_out = req.json()
        self.render("static/genericresp.html",msg=json_out['WS_MESSAGE']['WS_MESSAGE'])

class resourceRequestHandler(tornado.web.RequestHandler):
    def get(self, id):
        req = requests.get(base_url, headers=headers, auth=('ibmuser', 'ibmuser'), verify=False)
        self.write("Querying tweet with id " + str(req.content))

class queryStringRequestHandler(tornado.web.RequestHandler):
    def get(self):
        n = int(self.get_argument("n"))
        r = "odd" if n % 2 else "even"

        self.write("the number " + str(n) + " is " + r)

class staticRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/genericresp.html",msg="Something generic")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", basicRequestHandler),
        (r"/blog", staticRequestHandler),
        (r"/isEven", queryStringRequestHandler),
        (r"/tweet/([0-9]+)", resourceRequestHandler),
        (r"/postedform", postedForm)
    ])

    app.listen(port)
    # TODO remove in prod
    # tornado.autoreload.start()
    print("I'm listening on port specified")
    tornado.ioloop.IOLoop.current().start()
