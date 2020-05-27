#import http.server
#import socketserver
from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler
import os, sys, getopt

import glob2, pickle
import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from flask import Flask, request, render_template
import threading

base_URL = 'http://127.0.0.1'
main_port = 8000
flask_port = 5000
sflmt_dir = "output"

class HTTPHandler(SimpleHTTPRequestHandler):
    """This handler uses server.base_path instead of always using os.getcwd()"""
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.base_path, relpath)
        return fullpath

class HTTPServer(BaseHTTPServer):
    """The main server, you pass in base_path which is the path you want to serve requests from"""
    def __init__(self, base_path, server_address, RequestHandlerClass=HTTPHandler):
        self.base_path = base_path
        BaseHTTPServer.__init__(self, server_address, RequestHandlerClass)

try:
   opts, args = getopt.getopt(sys.argv, 'p:d:')
   print (opts)
except getopt.GetoptError:
   print ('sflmt-server.py -d <directory> -m <mainport> -f <flaskport>')
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
	   print ('sflmt-server.py -d <directory> -m <mainport> -f <flaskport>')
	   sys.exit()
   elif opt in ("-d"):
	   sflmt_dir = arg
   elif opt in ("-m"):
	   main_port = arg
   elif opt in ("-f"):
	   flask_port = arg

def mainServer():

    web_dir = os.path.join(os.path.dirname(__file__), sflmt_dir)
    httpd = HTTPServer(web_dir, ("", main_port))
    httpd.serve_forever()
'''
    #web_dir = os.path.join(os.path.dirname(__file__), str(path))
    #os.chdir(web_dir)
    #Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", int(main_port)), handler_from(path)) as httpd:
        print("serving " + str (path) + " at port", str(main_port))
        httpd.serve_forever()
'''

def flaskServer():

    # Read image features
    fe = FeatureExtractor()
    features = []
    img_paths = []
    for feature_path in glob2.glob(sflmt_dir + '/data/feature/*'):
        features.append(pickle.load(open(feature_path, 'rb')))
        img_paths.append(base_URL + ':' + str(main_port) + '/' + sflmt_dir + '/data/thumbs/' + os.path.splitext(os.path.basename(feature_path))[0] + '.jpg')
    #print (img_paths)

    #app = Flask(__name__, template_folder= './' + path + '/templates' )
    app = Flask(__name__, template_folder= sflmt_dir + '/templates/' )

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        if request.method == 'POST':
            file = request.files['query_img']
            img = Image.open(file.stream)  # PIL image
            base_img_path = '/assets/uploaded/' + datetime.now().isoformat() + "_" + file.filename
            uploaded_img_path = './' + sflmt_dir + base_img_path
            img.save(uploaded_img_path)
            query = fe.extract(img)
            dists = np.linalg.norm(features - query, axis=1)  # Do search
            ids = np.argsort(dists)[:30] # Top 30 results
            scores = [(dists[id], img_paths[id]) for id in ids]

            return render_template('search.html',
                                   query_path=(base_URL + ':' + str(main_port) + base_img_path),
                                   scores=scores)
        else:
            return render_template('search.html')

    app.run("0.0.0.0", port = flask_port)

if __name__ == "__main__":

    main_server = threading.Thread(target=mainServer)
    main_server.start()
    flaskServer()





'''
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('search.html')
    else:
        return render_template('search.html')

#app.run("0.0.0.0")

'''

'''
def main(argv):
    path = "./"
    port = 8000
    try:
       opts, args = getopt.getopt(argv, 'p:d:')
       print (opts)
    except getopt.GetoptError:
       print ('sflmt-server.py -d <directory> -p <port>')
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
    	   print ('sflmt-server.py -d <directory> -p <port>')
    	   sys.exit()
       elif opt in ("-d"):
    	   path = arg
       elif opt in ("-p"):
    	   port = arg

    web_dir = os.path.join(os.path.dirname(__file__), str(path))
    os.chdir(web_dir)

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", int(port)), Handler) as httpd:
       print("serving " + str (path) + " at port", str(port))
       httpd.serve_forever()


if __name__ == "__main__":
   main(sys.argv[1:])
'''
