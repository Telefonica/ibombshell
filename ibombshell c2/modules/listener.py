import re
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote
from module import Module
from warrior import Warrior
from config import Config
from printib import print_ok, print_info, print_error
try:
    from pynput.keyboard import Key, Controller
    PYINPUT = True
except:
    PYINPUT = False

# Send an enter to the keyboard to display the prompt
def enter_input():
    if PYINPUT:
        keyboard = Controller()
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

class Listener(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        warrior_path = Config.get_instance().get_warrior_path() + "ibs-"
        ipSrc = self.client_address[0]
        #regex = re.findall(r'^(.+)/([^/]+)$', self.path)
        admin = None
        os_version = None
        os_arch = None
        try:
            regex = re.findall(r'^(.+)/([^/]+)/([^/]+)/([^/]+)/([^/]+)$', self.path)
            admin = regex[0][2]
            os_version = unquote(regex[0][3]).strip("\r\n")
            os_arch = unquote(regex[0][4]).strip("\r\n")
        except:
            regex = re.findall(r'^(.+)/([^/]+)$', self.path)

        route = ''
        try:
            route = regex[0][0]
            routeId = regex[0][1]
        except Exception:
            print_error('Error creating warrior...')

        a = ''
        if route == "/ibombshell":
            try:
                with open('{}{}'.format(warrior_path, routeId), 'r') as f:
                    a = f.read()

                if a is not '':
                    print("")
                    print_ok('Warrior {} get iBombShell commands...'.format(routeId))
                    with open('{}{}'.format(warrior_path, routeId), 'w') as f:
                        f.write('')
                else:
                    Warrior.get_instance().review_status(routeId)
            except Exception:
                print_error('Warrior {} don\'t found'.format(routeId), start="\n")
        elif route == "/newibombshell":
            if not Warrior.get_instance().exist_warrior(routeId):
                with open('{}{}'.format(warrior_path, routeId), 'w') as f:
                    f.write('')
                
                is_admin = False
                if admin and admin == "admin":
                    is_admin = True
                print("")
                print_ok ("New warrior {} from {}".format(routeId, ipSrc))
                Warrior.get_instance().add_warrior(routeId, ipSrc, is_admin, os_version, os_arch)
            else:
                print_error('Warrior already exists!')
            enter_input()
        
        self._set_response()
        #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        self.wfile.write(a.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        self._set_response()
        self.wfile.write(''.encode('utf-8'))

        # results = post_data[8:].decode("utf-8")
        try:
            post_data = post_data.decode()
            fields = parse_qs(post_data)

            if fields:
                results = fields['results'][0]
                try:
                    url = str(unquote(results))
                    for result in url.split("\\n"):
                        print_info (result)
                except Exception:
                    if results is not '':
                        print_info (results)
                    else:
                        print_error('Error reading results!')
        except Exception as e:
            print_error('Error parsing the result!')
       
        enter_input()

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
            enter_input()
        except:
            print("The listener already exists ...")

    def run(self, server_class=HTTPServer, handler_class=Listener, address=None, port=8080): 
        server_address = (address, port)
        httpd = server_class(server_address, handler_class)
        print_info('Starting listener on {}:{}...'.format(address, port), start="\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        print_info('Stopping listener...')