import os
import json
import requests
import tornado.web
import tornado.ioloop
import tornado.autoreload

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

class landingPage(tornado.web.RequestHandler):
    def get(self):
        self.render("static/indexx.html")

class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/register.html")

class regRequ(tornado.web.RequestHandler):
    def post(self):
        base_url = 'https://192.86.33.94:19443/cbs/cusreg?AcctNo='
        # 100000001001 is the only working answer
        headers = {'Content-Type': 'application/json'}
        end_url= base_url+str(self.get_body_argument("accnt"))
        req = requests.get(end_url, headers=headers, auth=('ibmuser', 'ibmuser'), verify=False)
        json_out = req.json()
        self.render("static/genericresp.html",msg=json_out['CSRGRES']['CSRGRES']['MESSAGES'],cname=json_out['CSRGRES']['CSRGRES']['CUSTOMER_NAME'],cid=json_out['CSRGRES']['CSRGRES']['CUSTOMER_ID'],date=json_out['CSRGRES']['CSRGRES']['SYS_DATE'],time=json_out['CSRGRES']['CSRGRES']['SYS_TIME'])

class basicDeRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/deregister.html")

class deRegRequ(tornado.web.RequestHandler):
    def post(self):
        # base_url = 'https://192.86.33.94:19443/cusdereg/AccountNo?acctno='
        base_url = 'https://192.86.33.94:19443/cbscs/cusdereg?AcctNo='
        # 100000001001 is the only working answer
        headers = {'Content-Type': 'application/json'}
        end_url= base_url+str(self.get_body_argument("accnt"))
        req = requests.get(end_url, headers=headers, auth=('ibmuser', 'ibmuser'), verify=False)
        json_out = req.json()
        self.render("static/genericresp.html",msg=json_out['CSDGRES']['CSRGRES']['MESSAGES'],cname=json_out['CSDGRES']['CSRGRES']['CUSTOMER_NAME'],cid=json_out['CSDGRES']['CSRGRES']['CUSTOMER_ID'],date=json_out['CSDGRES']['CSRGRES']['SYS_DATE'],time=json_out['CSDGRES']['CSRGRES']['SYS_TIME'])

class basicPayHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/pay.html")

class payRequ(tornado.web.RequestHandler):
    def post(self):
        # base_url = 'https://192.86.33.94:19443/cuspymtauth/cuspay?debitamt='
        base_url = 'https://192.86.33.94:19443/cuspymtauth/cuspay?debitamt='
        # 100000001001 is the only working answer
        headers = {'Content-Type': 'application/json'}
        end_url= base_url+str(self.get_body_argument("debit_amt"))+"&acctno="+str(self.get_body_argument("accnt"))
        req = requests.get(end_url, headers=headers, auth=('ibmuser', 'ibmuser'), verify=False)
        json_out = req.json()
        self.render("static/genericresp.html",msg=json_out['CSPYRES']['CSPYRES']['MESSAGES'],cname=json_out['CSPYRES']['CSPYRES']['CUSTOMER_NAME'],hbal=json_out['CSPYRES']['CSPYRES']['HOLD_BALANCE'],lbal=json_out['CSPYRES']['CSPYRES']['LEDGER_BL'],bal=json_out['CSPYRES']['CSPYRES']['AVAILABLE_BALANCE'],cid=json_out['CSPYRES']['CSPYRES']['CUSTOMER_ID'],damt=json_out['CSPYRES']['CSPYRES']['DEBIT_AMOUNT_RES'],tid=json_out['CSPYRES']['CSPYRES']['TRANSACTION_ID'],date=json_out['CSPYRES']['CSPYRES']['SYS_DATE'],time=json_out['CSPYRES']['CSPYRES']['SYS_TIME'])

class basicRevHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/reversal.html")

class revRequ(tornado.web.RequestHandler):
    def post(self):
        # base_url = 'https://192.86.33.94:19443/cusdereg/AccountNo?acctno='
        base_url = 'https://192.86.33.94:19443/cuspymtrev/cuspayrev?acctono='
        # 100000001001 is the only working answer
        headers = {'Content-Type': 'application/json'}
        end_url= base_url+str(self.get_body_argument("accnt"))+"&tranid="++str(self.get_body_argument("trans"))+"&revamt="++str(self.get_body_argument("debit_amt"))
        req = requests.get(end_url, headers=headers, auth=('ibmuser', 'ibmuser'), verify=False)
        json_out = req.json()
        self.render("static/genericresp.html",msg=json_out['CSREVRES']['CSREVRES']['MESSAGES'],cname=json_out['CSREVRES']['CSREVRES']['CUSTOMER_NAME'],hbal=json_out['CSREVRES']['CSREVRES']['HOLD_BALANCE'],lbal=json_out['CSREVRES']['CSREVRES']['LEDGER_BL'],bal=json_out['CSREVRES']['CSREVRES']['AVAILABLE_BALANCE'],cid=json_out['CSREVRES']['CSREVRES']['CUSTOMER_ID'],credamt=json_out['CSREVRES']['CSREVRES']['CREDIT_AMOUNT_RES'],tid=json_out['CSREVRES']['CSREVRES']['TRANSACTIONS_ID'],date=json_out['CSREVRES']['CSREVRES']['SYS_DATE'],time=json_out['CSREVRES']['CSREVRES']['SYS_TIME'])

# class resourceRequestHandler(tornado.web.RequestHandler):
#     def get(self, id):
#         req = requests.get(base_url, headers=headers, auth=('ibmuser', 'ibmuser'), verify=False)
#         self.write("Querying tweet with id " + str(req.content))
#
# class queryStringRequestHandler(tornado.web.RequestHandler):
#     def get(self):
#         n = int(self.get_argument("n"))
#         r = "odd" if n % 2 else "even"
#
#         self.write("the number " + str(n) + " is " + r)
#
# class staticRequestHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.render("static/genericresp.html",msg="Something generic")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", landingPage),
        (r"/register", basicRequestHandler),
        (r"/regrequ", regRequ),
        (r"/deregister", basicDeRequestHandler),
        (r"/deregrequ", deRegRequ),
        (r"/paymentauth", basicPayHandler),
        (r"/payrequ", payRequ),
        (r"/paymentrevauth", basicRevHandler),
        (r"/payrevrequ", revRequ),
        # (r"/blog", staticRequestHandler),
        # (r"/isEven", queryStringRequestHandler),
        # (r"/tweet/([0-9]+)", resourceRequestHandler),
    ])

    app.listen(port)
    # TODO remove in prod
    tornado.autoreload.start()
    print("I'm listening on port specified")
    tornado.ioloop.IOLoop.current().start()
